# course/06-production/test_modules.py
import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import modules as M


class Registry(unittest.TestCase):
    def test_ids_are_unique_and_folders_exist(self):
        self.assertEqual(len(M.IDS), len(set(M.IDS)))
        for m in M.MODULES:
            self.assertTrue((M.CONTENT / m.folder).is_dir(), m.folder)
            self.assertTrue(m.folder.startswith(m.id + "-"), m.folder)

    def test_tags(self):
        self.assertEqual(M.tag("m05"), "M5")
        self.assertEqual(M.tag("m00"), "M0")
        self.assertEqual(M.tag("l1"), "L1")
        self.assertEqual(M.number("l1"), 1)
        self.assertEqual(M.family("l1"), "ladder")
        self.assertEqual(M.family("m09"), "deep")

    def test_next_stays_in_family(self):
        self.assertEqual(M.next_id("m04"), "m05")
        self.assertIsNone(M.next_id("m09"))

    def test_kicker(self):
        self.assertEqual(M.kicker("m05", "en"), "Module 5")
        self.assertEqual(M.kicker("m05", "zh"), "模块 5")
        self.assertEqual(M.kicker("l1", "en"), "Ladder step 1")
        self.assertEqual(M.kicker("l1", "zh"), "阶梯第 1 级")

    def test_expected_units_for_the_deep_modules(self):
        deep = [m for m in M.MODULES if m.family == "deep"]
        self.assertEqual(sum(4 + m.segments[0] for m in deep), 70)

    def test_ladder_modules_declare_smaller_checks(self):
        for m in M.MODULES:
            if m.family == "ladder":
                self.assertEqual(m.quiz, (4, 5))
                self.assertEqual(m.segments, (3, 4))
                self.assertFalse(m.figures)


if __name__ == "__main__":
    unittest.main()
