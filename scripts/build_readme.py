#!/usr/bin/env python3
"""Draw the project's state as the first thing a visitor sees.

Why this exists: a reader decides in about four seconds whether a repository
is worth their attention. Four seconds is not enough to read a paragraph, but
it is enough to read four numbers. So the numbers go first.

Why it is GENERATED and not written: those numbers already live in the private
vault's live board, which is the single source of truth for "is this built".
Written a second time by hand, the two start drifting on the very next change
— and a public page claiming a state the project left behind is worse than no
page at all.

Why the badge is OUR OWN SVG and not a badge service: this vault argues that
outside software is a tool that detaches at any time. A README whose header
collapses into broken images when someone else's CDN has a bad day fails its
own argument. Ours renders from a file in this repository, works offline in a
clone, and costs the reader zero third-party requests.

The input is board.json, exported from the vault with:

    python3 scripts/build_board.py --json > board.json

Only integers cross that boundary — never a component, machine or decision
name. The boundary is kept by the shape of the file, not by care.

Run from the vault root:  python3 scripts/build_readme.py
                          python3 scripts/build_readme.py --check
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOARD = ROOT / "board.json"
PATTERNS = ROOT / "patterns.json"
README = ROOT / "README.md"
ASSETS = ROOT / "assets"

# Every image this script owns. Named once, so adding a third cannot be
# half-done: it is written, checked for staleness and listed from here.
DRAWINGS = ("board", "patterns")

START = "<!-- board:start -->"
END = "<!-- board:end -->"

# Two palettes, one geometry. GitHub serves the matching image through
# <picture>, so the header follows the reader's theme instead of fighting it.
THEMES = {
    "light": {
        "bg": "#ffffff", "edge": "#d8dee6", "ink": "#1a1f27",
        "dim": "#6b7686", "rail": "#eaeef3",
    },
    "dark": {
        "bg": "#0d1117", "edge": "#222b36", "ink": "#e6eaf0",
        "dim": "#7c8899", "rail": "#161d27",
    },
}

# The same colours the vault's own board uses, so the two read as one system.
WORKING, PARTIAL, NOT_BUILT, DECIDED = "#2ecc71", "#f39c12", "#64748b", "#22a06b"

# The pattern classes are named, not proven. They get the project's own
# accent rather than a status colour: a green badge would read as "working"
# and that is precisely what they are not.
PATTERN_INK = "#f0b429"

W, H = 880, 172
PAD = 28


def bar(counts: list[tuple[int, str]], total: int, y: int, rail: str) -> str:
    """One proportional rail. Segments in order, no gaps, no rounding drift."""
    span = W - 2 * PAD
    out = [f'<rect x="{PAD}" y="{y}" width="{span}" height="8" rx="4" fill="{rail}"/>']
    x = float(PAD)
    for value, colour in counts:
        if not value:
            continue
        width = span * value / total
        out.append(
            f'<rect x="{x:.1f}" y="{y}" width="{width:.1f}" height="8" fill="{colour}"/>'
        )
        x += width
    # The rail's rounded ends are re-cut over the segments, so the bar keeps
    # its pill shape however the first and last segments happen to fall.
    out.append(
        f'<rect x="{PAD}" y="{y}" width="{span}" height="8" rx="4" fill="none" '
        f'stroke="{rail}" stroke-width="0"/>'
    )
    return "".join(out)


def svg(data: dict, theme: str) -> str:
    t = THEMES[theme]
    total = data["total_rows"]
    segments = [
        (data["working"], WORKING),
        (data["decisions"], DECIDED),
        (data["partial"], PARTIAL),
        (data["not_built"], NOT_BUILT),
    ]

    columns = [
        (data["working"], "working or proven", WORKING),
        (data["partial"], "partial", PARTIAL),
        (data["not_built"], "not built", NOT_BUILT),
        (data["decisions"], "decisions taken", DECIDED),
    ]
    step = (W - 2 * PAD) / len(columns)

    numbers = []
    for index, (value, label, colour) in enumerate(columns):
        cx = PAD + step * index + step / 2
        numbers.append(
            f'<text x="{cx:.0f}" y="96" text-anchor="middle" font-size="38" '
            f'font-weight="600" fill="{colour}">{value}</text>'
            f'<text x="{cx:.0f}" y="116" text-anchor="middle" font-size="11.5" '
            f'letter-spacing="0.08em" fill="{t["dim"]}">{label.upper()}</text>'
        )

    patterns = data["validated_patterns"]
    verdict = (
        f"{patterns} validated pattern{'' if patterns == 1 else 's'} "
        f"· the measure at this stage is honesty, not return"
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" \
viewBox="0 0 {W} {H}" role="img" aria-label="ORBITRON state: \
{data['working']} working, {data['partial']} partial, \
{data['not_built']} not built, {data['decisions']} decisions, \
{patterns} validated patterns">
<style>text{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,\
Helvetica,Arial,sans-serif}}</style>
<rect width="{W}" height="{H}" rx="10" fill="{t['bg']}" stroke="{t['edge']}"/>
<text x="{PAD}" y="34" font-size="12" letter-spacing="0.16em" \
fill="{t['dim']}">ORBITRON · STATE OF THE BUILD</text>
<text x="{W - PAD}" y="34" text-anchor="end" font-size="11.5" \
fill="{t['dim']}">{data['generated']}</text>
{bar(segments, total, 50, t['rail'])}
{''.join(numbers)}
<line x1="{PAD}" y1="134" x2="{W - PAD}" y2="134" stroke="{t['edge']}"/>
<text x="{W // 2}" y="155" text-anchor="middle" font-size="12.5" \
fill="{t['dim']}">{verdict}</text>
</svg>
"""


def patterns_svg(data: dict, theme: str) -> str:
    """One strip of name badges, drawn rather than fetched.

    Each badge carries a name and a version and nothing else. The class code
    and what the class looks for stay in the private vault: those say what the
    system reacts to, and that is the part this vault withholds.

    Widths are computed from the text, not guessed, so a longer name added
    later does not overflow its pill.
    """
    t = THEMES[theme]
    gap, pad, height = 10, 15, 30
    # An average glyph advance for the sizes used below. Measured off the
    # rendered strip rather than taken from the font metrics — close enough
    # that the padding stays visually even across all five names.
    widths = [
        int(len(p["name"]) * 7.4 + len(p["version"]) * 6.1 + pad * 2 + 16)
        for p in data["patterns"]
    ]
    width = sum(widths) + gap * (len(widths) - 1)

    badges, x = [], 0
    for pattern, w in zip(data["patterns"], widths):
        badges.append(
            f'<g transform="translate({x},0)">'
            f'<rect width="{w}" height="{height}" rx="15" fill="{PATTERN_INK}14" '
            f'stroke="{PATTERN_INK}55"/>'
            f'<text x="{pad}" y="20" font-size="13" font-weight="600" '
            f'fill="{PATTERN_INK}">{pattern["name"]}</text>'
            f'<text x="{w - pad}" y="20" text-anchor="end" font-size="11.5" '
            f'fill="{t["dim"]}">{pattern["version"]}</text>'
            f"</g>"
        )
        x += w + gap

    names = ", ".join(f'{p["name"]} {p["version"]}' for p in data["patterns"])
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Named pattern classes: {names}">
<style>text{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif}}</style>
{''.join(badges)}
</svg>
"""


def drawing(name: str, data: dict, patterns: dict, theme: str) -> str:
    return svg(data, theme) if name == "board" else patterns_svg(patterns, theme)


def block(data: dict, patterns: dict) -> str:
    """The README section between the markers.

    Every image is followed by the same information as text, because a
    picture is not readable by everyone and GitHub does not always load one.
    """
    total = data["total_rows"]
    names = " &nbsp;·&nbsp; ".join(
        f'**{p["name"]}** {p["version"]}' for p in patterns["patterns"]
    )
    count = len(patterns["patterns"])
    return f"""{START}
<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/board-dark.svg">
  <img src="assets/board-light.svg" alt="ORBITRON — state of the build: \
{data['working']} working or proven, {data['partial']} partial, \
{data['not_built']} not built, {data['decisions']} decisions taken, \
{data['validated_patterns']} validated patterns" width="880">
</picture>

**{data['working']}** working or proven &nbsp;·&nbsp; \
**{data['partial']}** partial &nbsp;·&nbsp; \
**{data['not_built']}** not built &nbsp;·&nbsp; \
**{data['decisions']}** decisions taken &nbsp;·&nbsp; \
**{data['validated_patterns']}** validated patterns

<sub>Generated from the project's live board on {data['generated']} \
— not written by hand. The bar spans all {total} tracked rows; its unfilled \
tail is work that is deferred, archived or deliberately closed.</sub>

&nbsp;

**The named pattern classes**

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/patterns-dark.svg">
  <img src="assets/patterns-light.svg" alt="Named pattern classes: \
{', '.join(p['name'] + ' ' + p['version'] for p in patterns['patterns'])}">
</picture>

{names}

<sub>Named after real exoplanets — one planet, one class. \
{count} classes are **designed**; none has been measured yet, and what each \
one looks for is not published. The names exist so the work has something \
to be called.</sub>

</div>
{END}"""


def main() -> None:
    data = json.loads(BOARD.read_text(encoding="utf-8"))
    patterns = json.loads(PATTERNS.read_text(encoding="utf-8"))
    readme = README.read_text(encoding="utf-8")
    fresh = block(data, patterns)

    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    found = pattern.search(readme)
    if not found:
        sys.exit(f"❌ README.md has no {START} … {END} block to fill.")

    def stale() -> list[str]:
        out = []
        for name in DRAWINGS:
            for theme in THEMES:
                file = ASSETS / f"{name}-{theme}.svg"
                if not file.exists() or file.read_text(
                    encoding="utf-8"
                ) != drawing(name, data, patterns, theme):
                    out.append(f"assets/{name}-{theme}.svg")
        return out

    if "--check" in sys.argv:
        problems = ([] if found.group(0) == fresh else ["README.md"]) + stale()
        if problems:
            sys.exit(
                "❌ Older than the data behind them: " + ", ".join(problems) + "\n"
                "   Run: python3 scripts/build_readme.py"
            )
        print("✅ README.md and every drawing match board.json and patterns.json.")
        return

    for name in DRAWINGS:
        for theme in THEMES:
            (ASSETS / f"{name}-{theme}.svg").write_text(
                drawing(name, data, patterns, theme), encoding="utf-8"
            )
    README.write_text(pattern.sub(lambda _: fresh, readme), encoding="utf-8")
    print(
        f"✅ Board written — {data['working']} working · {data['partial']} partial · "
        f"{data['not_built']} not built · {data['decisions']} decisions · "
        f"{data['validated_patterns']} validated · "
        f"{len(patterns['patterns'])} named classes"
    )


if __name__ == "__main__":
    main()
