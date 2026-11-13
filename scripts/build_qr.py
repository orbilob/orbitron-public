#!/usr/bin/env python3
"""
build_qr.py — the page's address as a QR code, for a phone camera.

    python3 scripts/build_qr.py            # write assets/qr.svg and assets/qr.png
    python3 scripts/build_qr.py --check    # 1 when either file is not what the address gives

A QR code is the address written as squares. A phone camera reads it and offers
the link; nobody runs anything. The address lives once — `og:url` in
`site/index.html` — and both files are drawn from it, so a new address (a
domain, one day) is a new code by running this, and a stale code is red in
`check_vault.py` before it is published.

Dark squares on white in both themes, with the standard quiet zone of four
squares: a camera reads contrast, and an inverted code is one that some phones
refuse. Error correction M — about 15% of the code can be covered or smudged.
The output is the same bytes on every run (segno is deterministic), which is
what lets the check compare files instead of decoding them.
"""

from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path

import segno

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "site" / "index.html"
SVG, PNG = ROOT / "assets" / "qr.svg", ROOT / "assets" / "qr.png"
DARK, LIGHT = "#0b1220", "#ffffff"
OG_URL = re.compile(r'<meta property="og:url" content="([^"]+)">')


def page_url() -> str:
    """The one address of the page — `og:url` in `site/index.html`."""
    m = OG_URL.search(PAGE.read_text(encoding="utf-8"))
    if not m:
        raise SystemExit(f"{PAGE.relative_to(ROOT)}: no og:url — the QR code has no address to carry")
    return m.group(1)


def render(kind: str, url: str) -> bytes:
    """The code for `url`, as `svg` or `png` bytes."""
    code = segno.make(url, error="m", micro=False)
    out = io.BytesIO()
    if kind == "svg":
        code.save(out, kind="svg", scale=8, border=4, dark=DARK, light=LIGHT,
                  xmldecl=False, svgns=True, title="ORBITRON — the page", nl=True)
    else:
        code.save(out, kind="png", scale=10, border=4, dark=DARK, light=LIGHT)
    return out.getvalue()


def stale() -> list[str]:
    """The files that are missing or differ from what the address gives."""
    url = page_url()
    return [str(path.relative_to(ROOT)) for path, kind in ((SVG, "svg"), (PNG, "png"))
            if not path.is_file() or path.read_bytes() != render(kind, url)]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    p.add_argument("--check", action="store_true", help="compare only, write nothing")
    args = p.parse_args(argv)
    if args.check:
        bad = stale()
        for name in bad:
            print(f"❌ {name}: not the code of {page_url()} — run python3 scripts/build_qr.py")
        return 1 if bad else 0
    url = page_url()
    SVG.write_bytes(render("svg", url))
    PNG.write_bytes(render("png", url))
    print(f"✅ assets/qr.svg · assets/qr.png — {url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
