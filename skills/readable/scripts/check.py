#!/usr/bin/env python3
"""Flag what a script can decide about English text for the readable skill.

    check.py [--level default|light|strict] <file | ->

Prints one `path:line: rule: match` per finding and exits 1 when there is any,
0 when there is none, 2 on a usage error. Code blocks, inline code, URLs, front
matter and block quotes are never checked. Indented code is checked, so fence it. Text inside double quotes is exempt
from the word and phrase rules, because a text can discuss a phrase.

The script finds marks. It cannot judge composition (an answer in the last
line, a point said twice), so a clean run does not end the skill's own check.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Longest sentence allowed, in words. The skill's limit is 25; "default" allows
# the few words more that its 80% column allows.
LIMITS = {"strict": 25, "default": 28, "light": 30}

STOCK_WORDS = (
    "additionally", "arguably", "best-in-class", "crucial", "cutting-edge", "deep dive",
    "delve", "delves", "delving", "foster", "fosters", "fostering", "fundamentally",
    "garner", "garners", "garnered", "groundbreaking", "interplay", "intricate",
    "leverage", "leverages", "leveraging", "load-bearing", "meticulous", "meticulously",
    "nestled", "paradigm", "pivotal", "quietly", "remarkably", "renowned", "robust",
    "seamless", "seamlessly", "showcase", "showcases", "showcasing", "streamline",
    "streamlines", "streamlined", "synergy", "tapestry", "testament", "underscore",
    "underscores", "underscoring", "utilize", "utilizes", "utilizing", "vibrant",
    "world-class",
)

PHRASES = {
    "contrast": (
        r"\bnot just\b", r"\bnot only\b", r"\bnot merely\b",
        r"\b(?:it|this|that)(?:'s| is|'s) not\b[^.!?]*?[,.] ?(?:it|this|that)(?:'s| is)\b",
    ),
    "run-up": (
        r"\blet's (?:dive|break|unpack|explore)\b", r"\bhere's the (?:thing|kicker|catch)\b",
        r"\bhere's what\b", r"\bworth noting\b", r"\bit bears mentioning\b",
        r"(?:^|[.!?] )(?:importantly|interestingly|notably),", r"\bwithout further ado\b",
    ),
    "saying": (r"\bat its core\b", r"\bthe real question is\b", r"\bthe heart of the matter\b"),
    "inflation": (
        r"\bserves? as\b", r"\bstands? as\b", r"\bpivotal moment\b", r"\bplays? a key role\b",
        r"\bset(?:s|ting)? the stage\b", r"\bdespite these challenges\b",
        r"\bthe future looks bright\b", r"\bindelible mark\b", r"\bevolving landscape\b",
    ),
    "hedge": (r"\bcould potentially\b", r"\bmight arguably\b", r"\bpotentially possibly\b"),
    "figure": (r"\bthink of it (?:as|like)\b", r"\bimagine a world\b"),
    "residue": (
        r"\bgreat question\b", r"\bi hope this helps\b", r"\blet me know if\b",
        r"\byou(?:'re| are) absolutely right\b", r"\bgood catch\b", r"\bcertainly!",
        r"\bof course!", r"\bas of my last\b",
    ),
    "signpost": (
        r"\bin conclusion\b", r"\bto sum up\b", r"\bin summary\b",
        r"\bto answer your question\b",
    ),
}

FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE = re.compile(r"`[^`\n]*`")
LINK_TARGET = re.compile(r"\]\([^)\s]*\)")
URL = re.compile(r"(?:https?://|www\.)\S+")
HTML = re.compile(r"<[^>\n]+>|&[a-z]+;|&#\d+;")
QUOTED = re.compile(r'"[^"\n]*"')
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.*)$")
BULLET = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
BOLD_LABEL = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+\*\*[^*\n]+(?::\*\*|\*\*:)")
TABLE_ROW = re.compile(r"^\s*\|")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+")
WORD = re.compile(r"[A-Za-z0-9][\w'’./+-]*")
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
STOCK_RE = re.compile(
    r"(?<![\w-])(" + "|".join(re.escape(w) for w in sorted(STOCK_WORDS, key=len, reverse=True)) + r")(?![\w-])",
    re.IGNORECASE,
)
PHRASE_RES = [(rule, re.compile(p, re.IGNORECASE)) for rule, ps in PHRASES.items() for p in ps]
SMALL = {"a", "an", "and", "as", "at", "but", "by", "for", "if", "in", "of", "on", "or", "the", "to", "vs", "via", "with"}


def prose_lines(text: str):
    """Yield (line number, line) for prose, with code, links and markup blanked."""
    lines = text.split("\n")
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 1
                break
    fence = None
    for number, line in enumerate(lines[start:], start + 1):
        mark = FENCE.match(line)
        if fence:
            if mark and mark.group(1)[0] == fence[0] and len(mark.group(1)) >= len(fence):
                fence = None
            yield number, ""
            continue
        if mark:
            fence = mark.group(1)
            yield number, ""
            continue
        if line.lstrip().startswith(">"):
            yield number, ""
            continue
        for pattern in (INLINE_CODE, LINK_TARGET, URL, HTML):
            line = pattern.sub(" ", line)
        yield number, line


def title_case(heading: str) -> bool:
    """True for Every Word Capitalised. Two capitals can be a product name, so it takes three,
    or one capital on a small word such as "The"."""
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z'’-]*", heading)][1:]
    if any(w[0].isupper() and w.lower() in SMALL for w in words):
        return True
    rest = [w for w in words if w.lower() not in SMALL and not w.isupper()]
    return len(rest) >= 3 and all(w[0].isupper() for w in rest)


def check(text: str, level: str = "default") -> list[tuple[int, str, str]]:
    limit = LIMITS[level]
    found: list[tuple[int, str, str]] = []
    bold_labels: list[tuple[int, str]] = []
    paragraph: list[tuple[int, str]] = []

    def flush() -> None:
        if not paragraph:
            return
        first = paragraph[0][0]
        joined = " ".join(part.strip() for _, part in paragraph)
        for sentence in SENTENCE_END.split(joined):
            count = len(WORD.findall(sentence))
            if count > limit:
                found.append((first, "long-sentence", f"{count} words, limit {limit}: {sentence[:60].strip()}..."))
        paragraph.clear()

    for number, line in prose_lines(text):
        stripped = line.strip()
        if not stripped:
            flush()
            continue
        heading = HEADING.match(line)
        table = bool(TABLE_ROW.match(line))
        if heading or table or BULLET.match(line):
            flush()

        for match in re.finditer(r"[—–]|(?<=\S) --? (?=\S)", line):
            if not table or match.group().strip() in "—–":
                found.append((number, "dash", stripped[max(0, match.start() - 20): match.end() + 20].strip()))
        if ";" in line:
            found.append((number, "semicolon", stripped[:60]))
        for match in re.finditer(r"[“”‘→←⇒➜]", line):
            found.append((number, "typed-character", match.group()))

        unquoted = QUOTED.sub(" ", line)
        for match in STOCK_RE.finditer(unquoted):
            found.append((number, "stock-word", match.group(1)))
        for rule, pattern in PHRASE_RES:
            for match in pattern.finditer(unquoted):
                found.append((number, rule, match.group().strip()))

        if heading:
            title = heading.group(1)
            if title_case(title):
                found.append((number, "title-case-heading", title.strip()))
            if EMOJI.search(title):
                found.append((number, "decorated-heading", title.strip()))
            continue
        if BOLD_LABEL.match(line):
            bold_labels.append((number, stripped[:60]))
        if not table:
            paragraph.append((number, BULLET.sub("", line)))
    flush()

    # One bold label can be a real term. Three or more is the pattern.
    if len(bold_labels) >= 3:
        found.extend((number, "bold-label", sample) for number, sample in bold_labels)
    return sorted(found)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--level", choices=sorted(LIMITS), default="default")
    parser.add_argument("path", help="a text or Markdown file, or - for standard input")
    args = parser.parse_args(argv)
    try:
        text = sys.stdin.read() if args.path == "-" else Path(args.path).read_text(encoding="utf-8")
    except OSError as error:
        print(f"check.py: {error}", file=sys.stderr)
        return 2
    findings = check(text, args.level)
    name = "<stdin>" if args.path == "-" else args.path
    for number, rule, sample in findings:
        print(f"{name}:{number}: {rule}: {sample}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
