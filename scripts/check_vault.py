#!/usr/bin/env python3
"""Guard against a vault that quietly contradicts itself.

This vault claims, in "05 — HOW WE WORK", that documentation rot is fought
mechanically rather than by good intentions. A vault making that claim with no
guard of its own would be advertising, not practice.

Three checks, all of which have already caught real defects here:

  1. Broken internal links — a link pointing into nothing sends the reader to
     the wrong place with confidence.
  2. Wiki links — GitHub renders [[these]] as literal text, so navigation
     silently dies for anyone reading on the web rather than in Obsidian.
  3. Callout format — GitHub renders only five alert types, only uppercase,
     and only with the type alone on its line. Anything else shows the reader
     a raw "[!success]" in a grey box.
  4. Withheld vocabulary — two families of words this vault deliberately does
     not use: anything naming where operational credentials live, and the
     execution vocabulary. Both were removed once by hand; a guard is what
     stops them coming back one careless paragraph at a time.

Exit 0 = clean. Exit 1 = something to fix, and every line says where.

Run from the vault root:  python3 scripts/check_vault.py
"""

import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GITHUB_ALERTS = {"NOTE", "TIP", "IMPORTANT", "WARNING", "CAUTION"}

LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")

# Words this vault does not use, and why. The pattern is matched
# case-insensitively on whole words; the note is what the reader sees.
WITHHELD = {
    r"api[- ]?key": "names a credential",
    r"private key": "names a credential",
    r"secret key": "names a credential",
    r"access token": "names a credential",
    r"\bpassphrase\b": "names a credential",
    r"\bwallet\b": "names a credential store",
    r"\bkeyring\b": "names a credential store",
    r"\bfreqtrade\b": "execution vocabulary",
    r"\btrading\b": "execution vocabulary",
    r"\btrade[sd]?\b": "execution vocabulary",
    r"\bexchange\b": "execution vocabulary",
    r"\bleverage\b": "execution vocabulary",
    r"\bscalp\w*\b": "execution vocabulary",
    r"\bbroker\b": "execution vocabulary",
    r"\border book\b": "execution vocabulary",
}
WIKI = re.compile(r"\[\[[^\]]+\]\]")
CALLOUT = re.compile(r"^\s*>\s*\[!([^\]]+)\](.*)$")

findings: list[str] = []


def markdown_files() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts)


for path in markdown_files():
    where = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")

    # 1 — every relative link resolves to a file that exists
    for match in LINK.finditer(text):
        href = match.group(2)
        if href.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = path.parent / urllib.parse.unquote(href.split("#")[0])
        if not target.exists():
            findings.append(f"{where}: broken link → {href}")

    # 2 — no wiki links; GitHub shows them as raw text
    for match in WIKI.finditer(text):
        findings.append(f"{where}: wiki link (invisible on GitHub) → {match.group(0)}")

    # 4 — vocabulary this vault withholds, deliberately
    for pattern, why in WITHHELD.items():
        for match in re.finditer(pattern, text, re.IGNORECASE):
            line = text.count("\n", 0, match.start()) + 1
            findings.append(
                f"{where}:{line}: withheld word \"{match.group(0)}\" — {why}"
            )

    # 3 — callouts in the form GitHub actually renders
    for number, line in enumerate(text.split("\n"), start=1):
        match = CALLOUT.match(line)
        if not match:
            continue
        kind, trailing = match.group(1), match.group(2).strip()
        if kind not in GITHUB_ALERTS:
            findings.append(
                f"{where}:{number}: callout [!{kind}] is not one of "
                f"{'/'.join(sorted(GITHUB_ALERTS))}"
            )
        elif trailing:
            findings.append(
                f"{where}:{number}: callout [!{kind}] has a title beside it — "
                "GitHub needs the type alone on its line"
            )

count = len(markdown_files())

if findings:
    for finding in findings:
        print(f"  {finding}")
    print(f"\n❌ {len(findings)} finding(s) across {count} documents.")
    sys.exit(1)

print(f"✅ Clean — {count} documents, no broken links, "
      f"GitHub-safe, nothing withheld leaked.")
