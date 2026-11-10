"""The readable checker must go red on each rule and stay green on clean text."""

import importlib.util
import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "readable" / "scripts" / "check.py"
spec = importlib.util.spec_from_file_location("readable_check", SCRIPT)
check_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_module)


def rules(text, level="default"):
    return [rule for _, rule, _ in check_module.check(text, level)]


CLEAN = """---
description: front matter is skipped — even with a dash; and a semicolon
---

# Install the CLI

The gateway validates the token. Then it forwards the request to the service.

- Run the script.
- Read the output, then fix the errors that you find.

| Rule | 80% |
|---|---|
| Short sentences | A few words more are fine |

See [the design](docs/a--b.md) and https://example.com/a;b for the details.

```bash
echo "not just code — it's robust; really"
```

> A quoted line that delves into a robust tapestry — unchanged.

The word "leverage" is on the list, and so is the phrase "not just".
"""

RED = {
    "dash": "The migration — which took six weeks — is done.",
    "semicolon": "The cache is warm; the service starts.",
    "typed-character": "Set the flag to “true” first.",
    "stock-word": "The SDK leverages a robust cache.",
    "contrast": "It's not just a build tool.",
    "run-up": "Let's dive into the rate limits.",
    "saying": "At its core, the queue is a list.",
    "inflation": "The folder serves as the home of the settings.",
    "hedge": "This could potentially break the build.",
    "figure": "Think of it as a road for data.",
    "residue": "I hope this helps with the release.",
    "signpost": "In conclusion, the release is ready.",
    "title-case-heading": "## Understanding The Impact Of Modern Technology",
    "decorated-heading": "## 🚀 Install the tool",
    "bold-label": "- **Speed:** it is fast.\n- **Safety:** it is safe.\n- **Use:** it is simple.",
    "long-sentence": "The config file " + "that the app loads at startup " * 6 + "controls the cache.",
}


class ReadableCheck(unittest.TestCase):
    def test_clean_text_has_no_findings(self):
        self.assertEqual(check_module.check(CLEAN), [])

    def test_each_rule_goes_red(self):
        for rule, text in RED.items():
            with self.subTest(rule=rule):
                self.assertIn(rule, rules(text))

    def test_spaced_hyphen_and_double_hyphen_are_dashes(self):
        self.assertIn("dash", rules("The old cluster - finally - is gone."))
        self.assertIn("dash", rules("The old cluster -- finally -- is gone."))
        self.assertNotIn("dash", rules("A well-documented, long-term API."))

    def test_contrast_split_across_clauses(self):
        self.assertIn("contrast", rules("It's not a health check, it's the first defence."))
        self.assertNotIn("contrast", rules("The value is not set. Run the script."))

    def test_two_bold_labels_are_allowed(self):
        self.assertNotIn("bold-label", rules("- **CAUTION:** back up first.\n- **Note:** it takes a minute."))

    def test_product_name_heading_is_not_title_case(self):
        self.assertNotIn("title-case-heading", rules("## Running in Claude Code"))

    def test_sentence_limit_follows_the_level(self):
        text = " ".join(["word"] * 27) + "."
        self.assertNotIn("long-sentence", rules(text, "default"))
        self.assertIn("long-sentence", rules(text, "strict"))
        self.assertNotIn("long-sentence", rules(" ".join(["word"] * 30) + ".", "light"))
        self.assertIn("long-sentence", rules(" ".join(["word"] * 31) + ".", "light"))

    def test_a_wrapped_sentence_is_counted_whole(self):
        text = "\n".join([" ".join(["word"] * 10)] * 3) + "."
        self.assertIn("long-sentence", rules(text))

    def test_a_fence_line_with_text_does_not_close_the_block(self):
        text = "```\n```python\nx = 1  # robust — really; yes\n```\n"
        self.assertEqual(check_module.check(text), [])

    def test_exit_codes(self):
        import tempfile

        with tempfile.TemporaryDirectory() as folder:
            clean = Path(folder) / "clean.md"
            clean.write_text(CLEAN, encoding="utf-8")
            dirty = Path(folder) / "dirty.md"
            dirty.write_text("line one\n\n" + RED["dash"] + "\n", encoding="utf-8")
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(check_module.main([str(clean)]), 0)
                self.assertEqual(check_module.main([str(dirty)]), 1)
                self.assertEqual(check_module.main([str(Path(folder) / "missing.md")]), 2)
                binary = Path(folder) / "binary.md"
                binary.write_bytes(b"caf\xe9 \xff\xfe")
                self.assertEqual(check_module.main([str(binary)]), 2)
            self.assertIn("dirty.md:3: dash:", out.getvalue())


if __name__ == "__main__":
    unittest.main()
