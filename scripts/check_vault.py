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

print(f"✅ Clean — {count} documents, no broken links, GitHub-safe throughout.")
