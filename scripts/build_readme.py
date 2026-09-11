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
CHAIN = ROOT / "chain.json"
README = ROOT / "README.md"
ASSETS = ROOT / "assets"

# Every image this script owns. Named once, so adding a third cannot be
# half-done: it is written, checked for staleness and listed from here.
DRAWINGS = ("board", "chain", "patterns", "tagline")

# What the line under the title says. It is drawn rather than written because
# GitHub strips inline colour from markdown: an image is the only way to say
# something in the project's own amber.
TAGLINE = "A personal, hobby project"

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

# What each part of the chain does, in as few words as will fit under a card.
# The names come from the vault; these three lines are presentation and live
# here, where the drawing that uses them lives.
PILLAR_LINE = {
    "ORPROBE": "brings the material",
    "ORLAB": "says whether there is anything in it",
    "ORCORE": "gives the finding an identity",
}

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


def chain_svg(data: dict, theme: str) -> str:
    """The three parts of the chain, side by side, with what each one holds.

    Three cards and two arrows: a reader who sees only this picture should be
    able to say what the project does and in which direction it flows. Under
    them, the four stages that stand between a bare signal and anything worth
    acting on.

    Every name here is exported from the vault, never typed: the drawing is a
    view of chain.json and nothing else.
    """
    t = THEMES[theme]
    card_w, gap = 276, 26
    width = card_w * 3 + gap * 2
    card_h, stages_h = 196, 58
    height = card_h + stages_h

    cards = []
    for index, pillar in enumerate(data["pillars"]):
        x = index * (card_w + gap)
        rows = []
        for row, process in enumerate(pillar["processes"]):
            y = 86 + row * 34
            rows.append(
                f'<text x="16" y="{y}" font-size="13.5" font-weight="600" '
                f'fill="{t["ink"]}">{process["name"]}</text>'
                f'<text x="{card_w - 16}" y="{y}" text-anchor="end" '
                f'font-size="11" fill="{PATTERN_INK}">'
                f'{process["designation"]}</text>'
            )
        cards.append(
            f'<g transform="translate({x},0)">'
            f'<rect width="{card_w}" height="{card_h}" rx="10" '
            f'fill="{t["rail"]}" stroke="{t["edge"]}"/>'
            f'<text x="16" y="34" font-size="14" font-weight="700" '
            f'letter-spacing="0.06em" fill="{t["ink"]}">{pillar["name"]}</text>'
            f'<text x="16" y="53" font-size="12" font-style="italic" '
            f'fill="{PATTERN_INK}">{pillar["epithet"]}</text>'
            f'<line x1="16" y1="66" x2="{card_w - 16}" y2="66" '
            f'stroke="{t["edge"]}"/>'
            f'{"".join(rows)}'
            f'<text x="16" y="{card_h - 16}" font-size="11.5" '
            f'fill="{t["dim"]}">{PILLAR_LINE.get(pillar["name"], "")}</text>'
            f"</g>"
        )
        if index < 2:
            cards.append(
                f'<text x="{x + card_w + gap / 2:.0f}" y="{card_h / 2 + 6:.0f}" '
                f'text-anchor="middle" font-size="17" '
                f'fill="{t["dim"]}">&#9656;</text>'
            )

    step = width / len(data["stages"])
    stages = []
    for index, stage in enumerate(data["stages"]):
        cx = step * index + step / 2
        stages.append(
            f'<text x="{cx:.0f}" y="{card_h + 40}" text-anchor="middle" '
            f'font-size="11.5" fill="{t["dim"]}">'
            f'<tspan fill="{PATTERN_INK}">{index + 1}</tspan>  {stage}</text>'
        )

    spoken = " then ".join(p["name"] for p in data["pillars"])
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" \
height="{height}" viewBox="0 0 {width} {height}" role="img" \
aria-label="The chain: {spoken}. Then four stages: \
{", ".join(data["stages"])}.">
<style>text{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,\
Helvetica,Arial,sans-serif}}</style>
{"".join(cards)}
<text x="0" y="{card_h + 22}" font-size="10.5" letter-spacing="0.14em" \
fill="{t["dim"]}">AND THEN FOUR STAGES</text>
{"".join(stages)}
</svg>
"""


def tagline_svg(theme: str) -> str:
    """The line under the title, in the project's amber.

    The same colour in both themes, by the operator's choice on 2026-09-11.
    Worth knowing: this amber carries a contrast ratio under 2:1 on white, so
    on a light background it reads as a soft accent rather than as body text —
    which is what it is meant to be.
    """
    width, height = 560, 48
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" \
height="{height}" viewBox="0 0 {width} {height}" role="img" \
aria-label="{TAGLINE}">
<style>text{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,\
Helvetica,Arial,sans-serif}}</style>
<text x="{width // 2}" y="32" text-anchor="middle" font-size="23" \
font-weight="700" fill="{PATTERN_INK}">{TAGLINE}</text>
</svg>
"""


def drawing(name: str, data: dict, patterns: dict, chain: dict,
            theme: str) -> str:
    if name == "board":
        return svg(data, theme)
    if name == "chain":
        return chain_svg(chain, theme)
    if name == "patterns":
        return patterns_svg(patterns, theme)
    return tagline_svg(theme)


WORDS = ("no", "One", "Two", "Three", "Four", "Five", "Six",
         "Seven", "Eight", "Nine", "Ten")


def spelled(n: int) -> str:
    """Small numbers read as words in a sentence, as digits in a table."""
    return WORDS[n] if n < len(WORDS) else str(n)


def block(data: dict, patterns: dict, chain: dict) -> str:
    """The README section between the markers.

    The order is the argument: first what is built, then the machine that was
    built, then what is being run through it. Every image is followed by the
    same information as text, because a picture is not readable by everyone
    and GitHub does not always load one.
    """
    total = data["total_rows"]
    names = " &nbsp;·&nbsp; ".join(
        f'**{p["name"]}** {p["version"]}' for p in patterns["patterns"]
    )
    count = len(patterns["patterns"])
    parts = " &nbsp;▸&nbsp; ".join(
        f'**{p["name"]}** *{p["epithet"]}*' for p in chain["pillars"]
    )
    # Two spellings on purpose: the visible line wants the wide spacing of
    # &nbsp;, and alt text wants none of it — an entity in an attribute is
    # read out by a screen reader as the character it stands for, and a row
    # of stray non-breaking spaces is noise to someone who cannot see the
    # picture it describes.
    walk = " &nbsp;·&nbsp; ".join(
        " ▸ ".join(x["name"] for x in p["processes"]) for p in chain["pillars"]
    )
    spoken_walk = ". ".join(
        ", then ".join(x["name"] for x in p["processes"]) for p in chain["pillars"]
    )
    stages = " &nbsp;·&nbsp; ".join(
        f'**{i + 1}** {s}' for i, s in enumerate(chain["stages"])
    )
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

**The chain**

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/chain-dark.svg">
  <img src="assets/chain-light.svg" alt="The chain: {spoken_walk}. \
Then four stages: {', '.join(chain['stages'])}." width="880">
</picture>

{parts}

<sub>{walk}</sub>

<sub>And then four stages: {stages}</sub>

**→ [How the chain works](04%20%E2%80%94%20THE%20ENGINEERING/The%20chain%20of%20three.md)**

&nbsp;

**The named pattern classes**

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/patterns-dark.svg">
  <img src="assets/patterns-light.svg" alt="Named pattern classes: \
{', '.join(p['name'] + ' ' + p['version'] for p in patterns['patterns'])}">
</picture>

{names}

<sub>Named after real exoplanets — one planet, one class. \
{spelled(count)} classes are designed; none measured yet, and what each one \
looks for is not published. **The project is in active development.**</sub>

</div>
{END}"""


def main() -> None:
    data = json.loads(BOARD.read_text(encoding="utf-8"))
    patterns = json.loads(PATTERNS.read_text(encoding="utf-8"))
    chain = json.loads(CHAIN.read_text(encoding="utf-8"))
    readme = README.read_text(encoding="utf-8")
    fresh = block(data, patterns, chain)

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
                ) != drawing(name, data, patterns, chain, theme):
                    out.append(f"assets/{name}-{theme}.svg")
        return out

    if "--check" in sys.argv:
        problems = ([] if found.group(0) == fresh else ["README.md"]) + stale()
        if problems:
            sys.exit(
                "❌ Older than the data behind them: " + ", ".join(problems) + "\n"
                "   Run: python3 scripts/build_readme.py"
            )
        print("✅ README.md and every drawing match the data behind them.")
        return

    for name in DRAWINGS:
        for theme in THEMES:
            (ASSETS / f"{name}-{theme}.svg").write_text(
                drawing(name, data, patterns, chain, theme), encoding="utf-8"
            )
    README.write_text(pattern.sub(lambda _: fresh, readme), encoding="utf-8")
    print(
        f"✅ Written — {data['working']} working · {data['partial']} partial · "
        f"{data['not_built']} not built · {data['decisions']} decisions · "
        f"{data['validated_patterns']} validated · "
        f"{len(patterns['patterns'])} named classes · "
        f"{len(chain['pillars'])} parts of the chain"
    )


if __name__ == "__main__":
    main()
