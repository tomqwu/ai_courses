"""The term linker (#term-links): first use per part, never inside code, links or headings."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_terms as ST  # noqa: E402

ITEMS = [
    {"forms": ["repository", "repo"], "title": "Repository", "plain": "A project folder.", "everyday": "",
     "href": "g.html#r", "except": []},
    {"forms": ["model"], "title": "AI model", "plain": "The AI.", "everyday": "", "href": "g.html#m",
     "except": ["model answer"]},
    {"forms": ["API"], "title": "API", "plain": "A menu.", "everyday": "", "href": "g.html#a", "except": []},
]


def page(body: str) -> str:
    return f'<body><main id="content" class="app-content">{body}</main></body>'


class Linker(unittest.TestCase):
    def setUp(self):
        self.L = ST.Linker(ITEMS)

    def test_first_use_in_a_part_only(self):
        out = self.L.page(page("<p>Clone the repository. The repository is big.</p>"))
        self.assertEqual(out.count('class="term"'), 1)

    def test_each_part_starts_again(self):
        out = self.L.page(page('<section class="learn-section"><p>a repo</p></section>'
                               '<section class="learn-section"><p>a repo</p></section>'))
        self.assertEqual(out.count('class="term"'), 2)

    def test_never_in_code_links_or_headings(self):
        out = self.L.page(page('<h2>The repo</h2><p><code>repo</code> <a href="x">repo</a></p>'))
        self.assertEqual(out.count('class="term"'), 0)

    def test_whole_words_and_case(self):
        out = self.L.page(page("<p>reposition the api and the API</p>"))
        self.assertEqual(out.count('class="term"'), 1)
        self.assertIn(">API</a>", out)

    def test_except_phrase(self):
        out = self.L.page(page("<p>Model answer: shown after you write.</p>"))
        self.assertEqual(out.count('class="term"'), 0)

    def test_the_words_are_unchanged(self):
        import re
        src = page("<p>Clone the repository, then call the API.</p>")
        out = self.L.page(src)
        self.assertEqual(re.sub(r"<[^>]+>", "", out), re.sub(r"<[^>]+>", "", src))

    def test_card_attributes(self):
        out = self.L.page(page("<p>the repo</p>"))
        self.assertIn('data-term-plain="A project folder."', out)
        self.assertIn('href="g.html#r"', out)


class Basics(unittest.TestCase):
    def test_every_term_is_complete_in_both_languages(self):
        ids = set()
        for t in ST.basics():
            self.assertNotIn(t["id"], ids)
            ids.add(t["id"])
            for loc in (t, t["zh"]):
                for key in ("term", "match", "plain", "everyday"):
                    self.assertTrue(loc.get(key), f"{t['id']}: {key}")

    def test_watch_words_are_explained(self):
        forms = {f.lower() for t in ST.basics() for f in t["match"]}
        for w in ST.watch():
            self.assertIn(w.lower(), forms, f"watch word {w!r} has no Basics entry")


if __name__ == "__main__":
    unittest.main()
