"""Private, deterministic PhoMT source selection. No action labels are inferred."""

import argparse
import hashlib
import io
from itertools import zip_longest
import json
from pathlib import Path
import random
import tempfile
import unicodedata
import zipfile

from .phomt_audit import audit_phomt_zip


EXPECTED_SHA256 = "fd58972b5058b17d0823b78e6ce7dbb775243e156efa2ca222079dbdd76e6a2e"
TRAIN_MEMBERS = ("PhoMT/detokenization/train/train.en", "PhoMT/detokenization/train/train.vi")


def _canonical_text(text):
    return " ".join(unicodedata.normalize("NFC", text).casefold().split())


def _select_pairs(archive, *, count, seed, max_bytes):
    """Reservoir-sample paired UTF-8 lines from train only; never log their text."""
    rng = random.Random(seed)
    selected = []
    total = eligible = 0
    with archive.open(TRAIN_MEMBERS[0]) as en_raw, archive.open(TRAIN_MEMBERS[1]) as vi_raw:
        en_stream = io.TextIOWrapper(en_raw, encoding="utf-8", errors="strict")
        vi_stream = io.TextIOWrapper(vi_raw, encoding="utf-8", errors="strict")
        try:
            for line_number, (en, vi) in enumerate(zip_longest(en_stream, vi_stream), 1):
                if en is None or vi is None:
                    raise ValueError("PhoMT train language files have different line counts")
                total += 1
                en, vi = en.strip(), vi.strip()
                if not en or not vi or max(len(en.encode("utf-8")), len(vi.encode("utf-8"))) > max_bytes:
                    continue
                eligible += 1
                pair = {"source_line": line_number, "en": en, "vi": vi}
                if len(selected) < count:
                    selected.append(pair)
                else:
                    index = rng.randrange(eligible)
                    if index < count:
                        selected[index] = pair
        except UnicodeDecodeError:
            raise ValueError("PhoMT train contains invalid UTF-8; no text logged") from None
    # Reject duplicated sentences inside the chosen pool rather than inventing groups.
    unique = []
    seen_en, seen_vi = set(), set()
    for pair in sorted(selected, key=lambda item: item["source_line"]):
        en_key, vi_key = _canonical_text(pair["en"]), _canonical_text(pair["vi"])
        if en_key in seen_en or vi_key in seen_vi:
            continue
        seen_en.add(en_key)
        seen_vi.add(vi_key)
        unique.append(pair)
    return unique, total, eligible


def prepare_sources(archive_path, output_dir, *, count=160, seed=20261001, max_bytes=384):
    """Create private pending authoring packets after verifying the known archive.

    The archive is streamed, not extracted. Only the detokenized training pair
    is opened. Output must remain under this project's Git-ignored data root.
    """
    if type(count) is not int or not 1 <= count <= 1000:
        raise ValueError("source count must be an integer from 1 to 1000")
    if type(seed) is not int or type(max_bytes) is not int or not 1 <= max_bytes <= 4096:
        raise ValueError("seed and byte-length limit must be valid integers")
    data_root = Path(__file__).resolve().parents[1] / "data"
    output = Path(output_dir).resolve()
    if not output.is_relative_to(data_root.resolve()) or output == data_root.resolve():
        raise ValueError("PhoMT-derived output must be inside the project data directory")
    if output.exists():
        raise FileExistsError("intake output already exists; preserve it and choose a new directory")
    report = audit_phomt_zip(archive_path, verify_crc=False)
    if report["archive_sha256"] != EXPECTED_SHA256:
        raise ValueError("PhoMT SHA-256 differs from the approved archive; intake refused")
    if report["requires_pickle_conversion_review"]:
        raise ValueError("pickle members require a separate conversion review")
    with zipfile.ZipFile(archive_path) as archive:
        if not set(TRAIN_MEMBERS) <= set(archive.namelist()):
            raise ValueError("expected detokenized training members are missing")
        selected, total, eligible = _select_pairs(archive, count=count, seed=seed, max_bytes=max_bytes)
    if not selected:
        raise ValueError("no eligible source pairs were found")
    packets = []
    for pair in selected:
        packets.append({
            "schema_version": "tide-jepa-authoring-packet-v1",
            "packet_id": f"phomt-train-{pair['source_line']:07d}",
            "source_split": "train",
            "source_line": pair["source_line"],
            "source_pair": {"en": pair["en"], "vi": pair["vi"]},
            "provenance_ref": f"vinai/PhoMT@{report['file_revision']}:detokenization/train:{pair['source_line']}",
            "license_ref": "Obsidian/RMIT Hackathon/raw/PhoMT Permission Confirmation — 2026-10-01.md",
            "approval_status": "pending",
            "template_family_id": None,
            "semantic_frame": None,
            "records": [],
            "edge_pairs": [],
            "path_pairs": [],
            "reviews": [],
        })
    payload = "".join(json.dumps(packet, ensure_ascii=False, sort_keys=True) + "\n" for packet in packets)
    summary = {
        "schema_version": "tide-jepa-source-selection-v1",
        "archive_sha256": report["archive_sha256"],
        "file_revision": report["file_revision"],
        "members_read": list(TRAIN_MEMBERS),
        "source_split": "train",
        "seed": seed,
        "requested_candidates": count,
        "selected_candidates": len(packets),
        "train_pair_count": total,
        "eligible_pair_count": eligible,
        "max_source_utf8_bytes": max_bytes,
        "packets_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        "action_labels_inferred": False,
        "training_approved": False,
        "dev_test_members_read": False,
        "selection_note": "Seeded reservoir sample; selected-pool exact sentence deduplication only. Human/AI review must group near duplicates and semantic/template families before splitting.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".phomt-intake-", dir=output.parent) as temporary:
        staging = Path(temporary) / "packet"
        staging.mkdir()
        (staging / "authoring.jsonl").write_text(payload, encoding="utf-8")
        (staging / "selection.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        staging.rename(output)
    return summary


def main():
    parser = argparse.ArgumentParser(description="Prepare private PhoMT source packets without assigning actions")
    parser.add_argument("archive")
    parser.add_argument("output_dir")
    parser.add_argument("--count", type=int, default=160)
    parser.add_argument("--seed", type=int, default=20261001)
    parser.add_argument("--max-bytes", type=int, default=384)
    args = parser.parse_args()
    summary = prepare_sources(args.archive, args.output_dir, count=args.count, seed=args.seed, max_bytes=args.max_bytes)
    print(json.dumps(summary, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
