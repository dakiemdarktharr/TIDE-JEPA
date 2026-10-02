import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

TORCH_AVAILABLE = importlib.util.find_spec("torch") is not None
if TORCH_AVAILABLE:
    import torch

from tide_jepa import (
    Action,
    CorpusRecord,
    Inventory,
    ModelConfig,
    UTF8ByteTokenizer,
    build_batch,
    dataset_fingerprint,
    grouped_split,
    read_jsonl,
    validate_records,
    write_split_manifest,
)


class DataContractTests(unittest.TestCase):
    def setUp(self):
        self.action = Action("POLARITY", "NEGATIVE")
        self.inventory = Inventory(
            (self.action,),
            {
                "vi": frozenset((self.action,)),
                "en": frozenset((self.action,)),
                "cham_phan_rang": frozenset((self.action,)),
            },
        )
        self.tokenizer = UTF8ByteTokenizer()

    def make_record(
        self,
        record_id,
        group_id,
        *,
        language="vi",
        approval_status="approved",
        path_id=None,
        path_step=None,
        source_frame=None,
        target_frame=None,
    ):
        return CorpusRecord(
            record_id=record_id,
            split_group_id=group_id,
            language=language,
            source_text=f"Source {record_id}.",
            target_text=f"Target {record_id}.",
            source_frame_id=source_frame or f"{group_id}-source",
            target_frame_id=target_frame or f"{group_id}-target",
            action=self.action,
            provenance_ref="source-record-1",
            license_ref="license-record-1",
            approval_status=approval_status,
            path_id=path_id,
            path_step=path_step,
        )

    def test_utf8_byte_tokenizer_round_trips_vietnamese_and_unicode(self):
        samples = ("Tôi không thấy ngôi nhà.", "Hello, world!", "a\u0306", "ภาษาไทย")
        for sample in samples:
            with self.subTest(sample=sample):
                self.assertEqual(self.tokenizer.decode(self.tokenizer.encode(sample)), "ă" if sample == "a\u0306" else sample)
        self.assertEqual(self.tokenizer.vocab_size, 259)
        self.assertEqual(
            self.tokenizer.decode(self.tokenizer.encode("hi", add_bos=True, add_eos=True) + [0, 0]),
            "hi",
        )

    def test_tokenizer_rejects_invalid_special_tokens_and_padding_order(self):
        with self.assertRaises(ValueError):
            self.tokenizer.decode([1, 1, 100])
        with self.assertRaises(ValueError):
            self.tokenizer.decode([0, 100])
        with self.assertRaises(ValueError):
            self.tokenizer.decode([259])
        truncated_utf8 = self.tokenizer.encode("À")[:1]
        with self.assertRaises(UnicodeDecodeError):
            self.tokenizer.decode(truncated_utf8)
        self.assertEqual(self.tokenizer.decode(truncated_utf8, errors="replace"), "�")

    def test_unapproved_records_are_rejected_for_training_use(self):
        pending = self.make_record("pending", "event-pending", approval_status="pending")
        with self.assertRaisesRegex(ValueError, "not approved"):
            validate_records((pending,), self.inventory)
        with self.assertRaisesRegex(ValueError, "not approved"):
            grouped_split(
                (pending, self.make_record("b", "event-b"), self.make_record("c", "event-c")),
                self.inventory,
                seed=1,
            )
        self.assertEqual(validate_records((pending,), self.inventory, require_approved=False), (pending,))

    def test_jsonl_loader_checks_schema_approval_and_license(self):
        record = self.make_record("row-1", "event-1")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "records.jsonl"
            path.write_text(json.dumps(record.to_dict(), ensure_ascii=False) + "\n", encoding="utf-8")
            self.assertEqual(read_jsonl(path, self.inventory), (record,))

            path.write_text(json.dumps({**record.to_dict(), "approval_status": "pending"}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "not approved"):
                read_jsonl(path, self.inventory)

            path.write_text(json.dumps({**record.to_dict(), "schema_version": "unknown"}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "schema_version"):
                read_jsonl(path, self.inventory)

            unlicensed = {**record.to_dict(), "action": {"kind": "POLARITY", "value": "UNLICENSED"}}
            path.write_text(json.dumps(unlicensed), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "not approved for vi"):
                read_jsonl(path, self.inventory)

    def test_path_records_must_be_contiguous_and_share_a_split_group(self):
        first = self.make_record(
            "path-0", "event-path", path_id="path-1", path_step=0, source_frame="f0", target_frame="f1"
        )
        second = self.make_record(
            "path-1", "event-path", path_id="path-1", path_step=1, source_frame="f1", target_frame="f2"
        )
        self.assertEqual(validate_records((first, second), self.inventory), (first, second))
        discontinuous = self.make_record(
            "path-1", "event-path", path_id="path-1", path_step=1, source_frame="other", target_frame="f2"
        )
        with self.assertRaisesRegex(ValueError, "not continuous"):
            validate_records((first, discontinuous), self.inventory)
        split_leak = self.make_record(
            "path-1", "other-event", path_id="path-1", path_step=1, source_frame="f1", target_frame="f2"
        )
        with self.assertRaisesRegex(ValueError, "share one split group"):
            validate_records((first, split_leak), self.inventory)
        with self.assertRaisesRegex(ValueError, "at least two"):
            validate_records((first,), self.inventory)

    @unittest.skipUnless(TORCH_AVAILABLE, "PyTorch is required to materialize model batches")
    def test_builder_creates_model_batch_without_inferring_cross_language_pairs(self):
        records = (
            self.make_record(
                "vi-0", "event-1", path_id="path-1", path_step=0, source_frame="f0", target_frame="f1"
            ),
            self.make_record(
                "vi-1", "event-1", path_id="path-1", path_step=1, source_frame="f1", target_frame="f2"
            ),
            self.make_record(
                "en-0", "event-1", language="en", path_id="path-1", path_step=0, source_frame="f0", target_frame="f1"
            ),
            self.make_record(
                "en-1", "event-1", language="en", path_id="path-1", path_step=1, source_frame="f1", target_frame="f2"
            ),
        )
        cfg = ModelConfig(vocab_size=self.tokenizer.vocab_size, action_count=1, width=8, heads=2, max_length=64)
        batch = build_batch(records, cfg, self.inventory)
        self.assertEqual(batch.source.dtype, torch.long)
        self.assertEqual(len(batch.edges), 4)
        self.assertEqual(len(batch.paths), 2)
        self.assertEqual(batch.path_pairs, ())
        self.assertEqual(batch.decoder_input[:, 0].tolist(), [cfg.bos_id] * 4)
        batch.validate(cfg, self.inventory)

    @unittest.skipUnless(TORCH_AVAILABLE, "PyTorch is required to materialize model batches")
    def test_builder_marks_ordered_source_target_copy_spans(self):
        from dataclasses import replace
        record = self.make_record("copy", "copy-group", language="en")
        record = replace(record, source_text="Alex walks a dog now.",
                         target_text="Alex walked a dog yesterday.")
        cfg = ModelConfig(vocab_size=self.tokenizer.vocab_size, action_count=1, width=8,
                          heads=2, max_length=64)
        batch = build_batch((record,), cfg, self.inventory)
        copied = self.tokenizer.encode("Alex")
        self.assertTrue(batch.copy_mask[0, :len(copied)].all().item())
        self.assertFalse(batch.copy_mask[0, -1].item())

    @unittest.skipUnless(TORCH_AVAILABLE, "PyTorch is required to materialize model batches")
    def test_builder_rejects_unapproved_rows_and_byte_length_overflow(self):
        cfg = ModelConfig(vocab_size=self.tokenizer.vocab_size, action_count=1, width=8, heads=2, max_length=4)
        pending = self.make_record("pending", "event-1", approval_status="pending")
        with self.assertRaisesRegex(ValueError, "not approved"):
            build_batch((pending,), cfg, self.inventory)
        long_text = self.make_record("long", "event-2")
        with self.assertRaisesRegex(ValueError, "exceeds"):
            build_batch((long_text,), cfg, self.inventory)

    def test_grouped_split_is_deterministic_and_prevents_translation_leakage(self):
        records = []
        for group in range(12):
            records.append(self.make_record(f"vi-{group}", f"event-{group}", language="vi"))
            records.append(self.make_record(f"en-{group}", f"event-{group}", language="en"))
        first = grouped_split(records, self.inventory, seed=23)
        second = grouped_split(reversed(records), self.inventory, seed=23)
        changed = grouped_split(records, self.inventory, seed=24)
        self.assertEqual(first.to_dict(), second.to_dict())
        self.assertNotEqual(first.sha256, changed.sha256)
        self.assertEqual(set(first.record_ids), {"train", "validation", "test"})
        for record in records:
            assigned = first.groups[record.split_group_id]
            self.assertIn(record.record_id, first.record_ids[assigned])
        self.assertTrue(all(first.record_ids[name] for name in ("train", "validation", "test")))

    @unittest.skipUnless(TORCH_AVAILABLE, "PyTorch is required for padded teacher forcing")
    def test_builder_shifts_labels_after_padding_unequal_target_lengths(self):
        from dataclasses import replace
        rows = (replace(self.make_record("short", "event-short"), target_text="Có."),
                replace(self.make_record("long", "event-long"), target_text="Tôi không thấy một ngôi nhà ở đây."))
        cfg = ModelConfig(vocab_size=259, action_count=1, width=8, heads=2, max_length=128)
        batch = build_batch(rows, cfg, self.inventory)
        self.assertTrue(torch.equal(batch.decoder_input[:, 1:], batch.labels[:, :-1]))
        short_length = len(self.tokenizer.encode(rows[0].target_text, add_eos=True))
        self.assertEqual(batch.decoder_input[0, short_length].item(), self.tokenizer.eos_id)
        self.assertEqual(batch.labels[0, short_length].item(), self.tokenizer.pad_id)

    def test_fingerprint_is_order_independent_and_content_sensitive(self):
        first = self.make_record("a", "event-a")
        second = self.make_record("b", "event-b", language="en")
        self.assertEqual(dataset_fingerprint((first, second)), dataset_fingerprint((second, first)))
        changed = self.make_record("b", "event-b", language="en", target_frame="different")
        self.assertNotEqual(dataset_fingerprint((first, second)), dataset_fingerprint((first, changed)))

    def test_split_requires_independent_groups_and_valid_fractions(self):
        two = (self.make_record("a", "g1"), self.make_record("b", "g2"))
        with self.assertRaisesRegex(ValueError, "at least three"):
            grouped_split(two, self.inventory, seed=1)
        three = (*two, self.make_record("c", "g3"))
        with self.assertRaisesRegex(ValueError, "sum to one"):
            grouped_split(three, self.inventory, seed=1, train=0.7, validation=0.2, test=0.2)

    def test_fresh_grouped_split_rejects_cross_group_frame_and_text_leakage(self):
        from dataclasses import replace
        rows = [self.make_record(f"row-{i}", f"group-{i}") for i in range(3)]
        rows[1] = replace(rows[1], source_frame_id=rows[0].source_frame_id)
        with self.assertRaisesRegex(ValueError, "frame occurs"):
            grouped_split(rows, self.inventory, seed=3)
        rows = [self.make_record(f"row-{i}", f"group-{i}") for i in range(3)]
        rows[1] = replace(rows[1], source_text=rows[0].source_text)
        with self.assertRaisesRegex(ValueError, "sentence occurs"):
            grouped_split(rows, self.inventory, seed=3)

    def test_split_manifest_writes_atomically_as_json(self):
        records = [self.make_record(f"row-{i}", f"event-{i}") for i in range(3)]
        manifest = grouped_split(records, self.inventory, seed=5)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "split.json"
            write_split_manifest(path, manifest)
            loaded = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(loaded, manifest.to_dict())
            self.assertFalse(list(path.parent.glob("*.tmp")))


if __name__ == "__main__":
    unittest.main()
