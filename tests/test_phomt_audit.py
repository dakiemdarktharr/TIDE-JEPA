import json
from pathlib import Path
import stat
import tempfile
import unittest
import warnings
import zipfile

from tide_jepa.phomt_audit import audit_phomt_zip


class PhoMTAuditTests(unittest.TestCase):
    def make_zip(self, directory: str, entries: list[tuple[str, bytes]]) -> Path:
        path = Path(directory) / "PhoMT.zip"
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, content in entries:
                archive.writestr(name, content)
        return path

    def test_audit_reports_metadata_and_never_deserializes_pickle(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.make_zip(
                directory,
                [("train.pkl", b"not opened"), ("README.txt", b"metadata only")],
            )
            report = audit_phomt_zip(path)

        self.assertEqual(report["dataset"], "vinai/PhoMT")
        self.assertEqual(report["member_count"], 2)
        self.assertEqual(report["file_suffix_counts"], {".pkl": 1, ".txt": 1})
        self.assertEqual(report["pickle_members_not_deserialized"], ["train.pkl"])
        self.assertTrue(report["requires_pickle_conversion_review"])
        self.assertFalse(report["crc_checked"])
        self.assertEqual(len(report["archive_sha256"]), 64)
        json.dumps(report)

    def test_crc_check_streams_and_validates_member_data(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.make_zip(directory, [("pairs.tsv", b"en\tvi\nhello\txin chao\n")])
            report = audit_phomt_zip(path, verify_crc=True)
        self.assertTrue(report["crc_checked"])

    def test_rejects_non_zip_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "PhoMT.zip"
            path.write_bytes(b"not a zip")
            with self.assertRaisesRegex(ValueError, "must be a ZIP"):
                audit_phomt_zip(path)

    def test_rejects_path_traversal_and_absolute_members(self):
        unsafe_names = ("../outside.pkl", "C:\\outside.pkl", "/outside.pkl", "nested/../outside.pkl")
        for name in unsafe_names:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                path = self.make_zip(directory, [(name, b"x")])
                with self.assertRaises(ValueError):
                    audit_phomt_zip(path)

    def test_rejects_symlink_members(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "PhoMT.zip"
            info = zipfile.ZipInfo("link")
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr(info, "outside")
            with self.assertRaisesRegex(ValueError, "symbolic link"):
                audit_phomt_zip(path)

    def test_rejects_duplicate_normalized_paths_and_oversized_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                path = self.make_zip(directory, [("folder\\item.tsv", b"x"), ("folder/item.tsv", b"y")])
            with self.assertRaisesRegex(ValueError, "duplicate normalized path"):
                audit_phomt_zip(path)

        with tempfile.TemporaryDirectory() as directory:
            path = self.make_zip(directory, [("large.tsv", b"12345")])
            with self.assertRaisesRegex(ValueError, "uncompressed-size safety limit"):
                audit_phomt_zip(path, max_uncompressed_bytes=4)


if __name__ == "__main__":
    unittest.main()
