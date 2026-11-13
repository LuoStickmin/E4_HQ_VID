import json
import os
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

import nikon_movie_patch as patch  # noqa: E402

MODULE = Path(os.environ.get(
    "D7200_MODULE",
    ROOT.parent / "D7200_0104.dec.modules" / "b1230_104.bin",
))
PROFILE = ROOT / "profiles" / "d7200_hq64.json"
CURRENT_SHA = "c278c63419f82cacdc62d91670dbb95a75e10e21572464e730000567c37ef4dc"


@unittest.skipUnless(MODULE.is_file(),
                     "provide D7200_MODULE or ../D7200_0104.dec.modules/b1230_104.bin")
class D7200PatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = MODULE.read_bytes()
        cls.profile = json.loads(PROFILE.read_text(encoding="utf-8"))

    def test_profile_matches_current_state(self):
        out, changes, ranges = patch.apply_profile(self.module, self.profile)
        changed = patch.verify_scope(self.module, out, ranges)
        self.assertEqual(len(changes), 3)
        self.assertEqual(changed, 29)
        self.assertEqual(patch.sha256(out), CURRENT_SHA)

    def test_wrong_stock_rates_rejected(self):
        bad = bytearray(self.module)
        bad[0x2ACD9C:0x2ACDA0] = (1).to_bytes(4, "little")
        with self.assertRaises(ValueError):
            patch.apply_profile(bytes(bad), self.profile)

    def test_label_length_must_match(self):
        profile = {
            "table": self.profile["table"],
            "patches": [{
                "type": "utf16_label",
                "offset": 0x59B05C,
                "expect": "1920x1080; 60p",
                "value": "1080 60p Hq",  # one char shorter
            }],
        }
        with self.assertRaises(ValueError):
            patch.apply_profile(self.module, profile)


if __name__ == "__main__":
    unittest.main()
