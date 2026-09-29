"""Site feature flags (site-flags.json): pricing hides and shows the course's own prices."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_shell as SH  # noqa: E402
import site_paths as SP  # noqa: E402


class Pricing(unittest.TestCase):
    def glance(self, on: bool) -> str:
        real = SH.flag
        SH.flag = lambda name: on if name == "pricing" else real(name)
        try:
            return SP._at_a_glance([("Level", "Beginner"), ("Price", "$399")])
        finally:
            SH.flag = real

    def test_off_hides_the_price(self):
        html = self.glance(False)
        self.assertIn("Beginner", html)
        self.assertNotIn("$399", html)

    def test_on_shows_it(self):
        self.assertIn("$399", self.glance(True))

    def test_the_flag_file_reads(self):
        self.assertIsInstance(SH.flag("pricing"), bool)
        self.assertFalse(SH.flag("no-such-flag"))


if __name__ == "__main__":
    unittest.main()
