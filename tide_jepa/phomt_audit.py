"""Metadata-only safety and integrity checks for the gated PhoMT ZIP.

This module never extracts files or deserializes pickle content. It reports
archive metadata and hashes only; it does not create TIDE-JEPA training rows.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PureWindowsPath
import stat
import zipfile


PHOMT_REPOSITORY = "vinai/PhoMT"
PHOMT_FILE_REVISION = "aee99d07f0f5e6faf64b64f52adf314563350ce5"
DEFAULT_MAX_MEMBERS = 10_000
DEFAULT_MAX_UNCOMPRESSED_BYTES = 8 * 1024**3
PICKLE_SUFFIXES = {".pkl", ".pickle"}


def _safe_member_name(info: zipfile.ZipInfo) -> str:
    """Normalize and validate a ZIP member path without extracting it."""
    original = info.filename
    if not original or "\x00" in original:
        raise ValueError("archive contains an empty or null-byte member path")

    normalized = original.replace("\\", "/")
    windows_path = PureWindowsPath(original)
    if normalized.startswith("/") or windows_path.is_absolute() or windows_path.drive:
        raise ValueError(f"archive contains an absolute member path: {original!r}")

    parts = normalized.rstrip("/").split("/")
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise ValueError(f"archive contains an unsafe member path: {original!r}")

    mode = info.external_attr >> 16
    if stat.S_ISLNK(mode):
        raise ValueError(f"archive contains a symbolic link: {original!r}")
    if info.flag_bits & 0x1:
        raise ValueError(f"archive contains an encrypted member: {original!r}")
    return "/".join(parts)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_phomt_zip(
    archive_path: str | Path,
    *,
    verify_crc: bool = False,
    max_members: int = DEFAULT_MAX_MEMBERS,
    max_uncompressed_bytes: int = DEFAULT_MAX_UNCOMPRESSED_BYTES,
) -> dict[str, object]:
    """Audit PhoMT ZIP structure and provenance without extraction/unpickling.

    ``verify_crc`` streams archive members through ZIP's integrity check. The
    default is metadata-only and does not decompress any member contents.
    """
    path = Path(archive_path)
    if not path.is_file():
        raise FileNotFoundError(f"PhoMT archive does not exist: {path}")
    if max_members < 1 or max_uncompressed_bytes < 1:
        raise ValueError("archive limits must be positive")
    if not zipfile.is_zipfile(path):
        raise ValueError("PhoMT source must be a ZIP archive")

    members: list[dict[str, object]] = []
    normalized_names: set[str] = set()
    suffix_counts: Counter[str] = Counter()
    pickle_members: list[str] = []
    uncompressed_total = 0

    with zipfile.ZipFile(path, "r") as archive:
        infos = archive.infolist()
        if len(infos) > max_members:
            raise ValueError(f"archive has too many members: {len(infos)} > {max_members}")

        for info in infos:
            safe_name = _safe_member_name(info)
            if safe_name in normalized_names:
                raise ValueError(f"archive contains duplicate normalized path: {safe_name!r}")
            normalized_names.add(safe_name)
            if info.file_size < 0 or info.compress_size < 0:
                raise ValueError(f"archive has invalid size metadata for {safe_name!r}")
            uncompressed_total += info.file_size
            if uncompressed_total > max_uncompressed_bytes:
                raise ValueError(
                    "archive exceeds the configured uncompressed-size safety limit "
                    f"({uncompressed_total} > {max_uncompressed_bytes} bytes)"
                )

            suffix = Path(safe_name).suffix.lower() or "<none>"
            if not info.is_dir():
                suffix_counts[suffix] += 1
                if suffix in PICKLE_SUFFIXES:
                    pickle_members.append(safe_name)
            members.append({
                "path": safe_name,
                "is_directory": info.is_dir(),
                "compressed_bytes": info.compress_size,
                "uncompressed_bytes": info.file_size,
                "compression_method": info.compress_type,
            })

        crc_checked = False
        if verify_crc:
            bad_member = archive.testzip()
            if bad_member is not None:
                raise ValueError(f"ZIP CRC check failed for member: {bad_member!r}")
            crc_checked = True

    return {
        "dataset": PHOMT_REPOSITORY,
        "file_revision": PHOMT_FILE_REVISION,
        "archive_name": path.name,
        "archive_size_bytes": path.stat().st_size,
        "archive_sha256": _sha256_file(path),
        "member_count": len(members),
        "file_count": sum(not bool(member["is_directory"]) for member in members),
        "uncompressed_size_bytes": uncompressed_total,
        "file_suffix_counts": dict(sorted(suffix_counts.items())),
        "pickle_members_not_deserialized": sorted(pickle_members),
        "requires_pickle_conversion_review": bool(pickle_members),
        "crc_checked": crc_checked,
        "members": members,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit PhoMT ZIP metadata without extracting or unpickling it"
    )
    parser.add_argument("archive", help="path to data/raw/phomt/PhoMT.zip")
    parser.add_argument(
        "--verify-crc",
        action="store_true",
        help="stream every member to verify ZIP CRC integrity; still does not extract or unpickle",
    )
    args = parser.parse_args()
    report = audit_phomt_zip(args.archive, verify_crc=args.verify_crc)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
