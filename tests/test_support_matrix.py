import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

MODELS = ["D4S", "D750", "D810", "D810A", "D7200", "D5300",
          "D5500", "D5600", "D3300", "D3400", "D3500"]


class SupportMatrixTests(unittest.TestCase):
    def test_all_expeed4_dslrs_are_listed(self):
        text = (ROOT / "SUPPORT.md").read_text(encoding="utf-8")
        for model in MODELS:
            self.assertIn("| %s |" % model, text,
                          "%s missing from SUPPORT.md" % model)

    def test_readme_links_support_and_changelog(self):
        for name in ("README.md", "README.en.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("SUPPORT.md", text)
            self.assertIn("CHANGELOG.md", text)


if __name__ == "__main__":
    unittest.main()
