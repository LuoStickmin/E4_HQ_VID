import os
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

import scan_movie_modes as scan  # noqa: E402

CASES = [
    ("D7200", "D7200_MODULE", "b1230_104.bin", 0x2ACD8C, 0x59B05C, 0x6C9192),
    ("D750", "D750_MODULE", "b1010_115a.bin", 0x2AA99C, 0x754A96, 0x885E12),
    ("D810", "D810_MODULE", "b920_114.bin", 0x28B984, 0x6B0804, 0x7EF3DE),
    ("D3400", "D3400_MODULE", "b1480_113.bin", 0x335B00, 0x5F695A, 0x6D6200),
    ("D4S", "D4S_MODULE", "b1140_133f.bin", 0x262F48, 0x4E79EE, 0x6326BA),
    ("D5500", "D5500_MODULE", "b1120_102.bin", 0x2D0334, 0x57DE06, 0x64DBDC),
    ("D5600", "D5600_MODULE", "b1530_120.bin", 0x301C8C, 0x5BBDC8, 0x68BD18),
    ("D810A", "D810A_MODULE", "b1410_102b.bin", 0x28B940, 0x5CADEA, 0x7093CA),
]


class ScannerTests(unittest.TestCase):
    def test_scanner_finds_tables_and_labels(self):
        for model, env, default, base, en, zh in CASES:
            module = Path(os.environ.get(env, ROOT.parent / default))
            if not module.is_file():
                with self.subTest(model=model):
                    self.skipTest("%s not set and %s not found" % (env, module))
            with self.subTest(model=model):
                data = module.read_bytes()
                tables = scan.find_tables(data)
                self.assertTrue(tables, "no table found")
                self.assertEqual(tables[0]["base"], base)
                self.assertIn(en, scan.find_utf16(data, "1920x1080; 60p"))
                self.assertIn(zh, scan.find_utf16(data, "1920x1080;60p"))


if __name__ == "__main__":
    unittest.main()
