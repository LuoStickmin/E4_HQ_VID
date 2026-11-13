import json
import os
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

import nikon_movie_patch as patch  # noqa: E402

CASES = [
    ("d7200_hq64.json", "D7200_MODULE", "b1230_104.bin", 29),
    ("d750_hq64.json", "D750_MODULE", "b1010_115a.bin", 29),
    ("d810_hq64.json", "D810_MODULE", "b920_114.bin", 29),
    ("d3400_hq64.json", "D3400_MODULE", "b1480_113.bin", 69),
]


class ProfileTests(unittest.TestCase):
    def test_profiles(self):
        for name, env, default, expected in CASES:
            path = ROOT / "profiles" / name
            module = Path(os.environ.get(env, ROOT.parent / default))
            if not module.is_file():
                with self.subTest(profile=name):
                    self.skipTest("%s not set and %s not found" % (env, module))
            with self.subTest(profile=name):
                profile = json.loads(path.read_text(encoding="utf-8"))
                data = module.read_bytes()
                out, changes, ranges = patch.apply_profile(data, profile)
                changed = patch.verify_scope(data, out, ranges)
                self.assertEqual(changed, expected)
                self.assertGreaterEqual(len(changes), 3)
                table = profile["table"]
                rec = patch.read_record(out, table, 0)
                self.assertEqual((rec["rate_a"], rec["rate_b"]),
                                 (64_000_000, 60_000_000))

    def test_supported_profiles_exist(self):
        names = {p.name for p in (ROOT / "profiles").glob("*.json")}
        for name, _, _, _ in CASES:
            self.assertIn(name, names)


if __name__ == "__main__":
    unittest.main()
