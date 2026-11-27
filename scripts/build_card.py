#!/usr/bin/env python3
"""
build_card.py — the logo, the QR code and the address on one wide card.

    python3 scripts/build_card.py            # write assets/card.png
    python3 scripts/build_card.py --check    # 1 when the card does not carry the page's address

An avatar is cut into a small circle: an address written on it shrinks to dots,
and the circle clips the three corner squares a camera needs to read a QR code.
A wide picture keeps both whole — a cover image, a picture under an e-mail
signature. That is what this card is for; the avatar stays the plain logo.

1640 x 624 — the cover size of a social page; it scales down to a signature.
The content sits in the middle, because a phone shows the middle of a cover.
The background is the logo's own near-black, so the logo has no visible edge.

The address lives once — `og:url` in `site/index.html`, read through
`build_qr.page_url()` — and the card stores it in the PNG itself, as a text
chunk named `address`. The check reads that chunk with the standard library
only, so CI needs no image library and no font to tell a stale card: a new
address (a domain, one day) turns `check_vault.py` red until the card is
redrawn here.
"""

from __future__ import annotations

import argparse
import struct
import sys
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_qr  # noqa: E402  — same folder

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "assets" / "logo.png"
CARD = ROOT / "assets" / "card.png"
FONT = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
SIZE = (1640, 624)
BACKGROUND = (9, 11, 10)          # the logo's corner pixel
TEXT = (226, 232, 230)
MUTED = (150, 160, 158)
KEY = "address"
QR_SIDE = 330                     # the most the code may take, in pixels


def shown(url: str) -> str:
    """The address as a person types it — without the scheme and the last slash."""
    return url.split("://", 1)[-1].rstrip("/")


def draw(url: str) -> "object":
    """The card for `url`, as a Pillow image."""
    import io

    import segno
    from PIL import Image, ImageDraw, ImageFilter, ImageFont

    card = Image.new("RGB", SIZE, BACKGROUND)
    logo = Image.open(LOGO).convert("RGB")
    logo = logo.resize((int(logo.width * 560 / logo.height), 560), Image.LANCZOS)
    left = 250
    # The logo's field is a shade bluer than its corner: fade its edges into
    # the card, or it shows as a box.
    fade = Image.new("L", logo.size, 0)
    ImageDraw.Draw(fade).rectangle((60, 60, logo.width - 60, logo.height - 60), fill=255)
    fade = fade.filter(ImageFilter.GaussianBlur(30))
    card.paste(logo, (left, (SIZE[1] - logo.height) // 2), fade)

    # Whole pixels per square: a code scaled by a fraction gets uneven squares,
    # and some cameras refuse it.
    code = segno.make(url, error="m", micro=False)
    width = code.symbol_size(scale=1, border=4)[0]
    buf = io.BytesIO()
    code.save(buf, kind="png", scale=QR_SIDE // width, border=4,
              dark=build_qr.DARK, light=build_qr.LIGHT)
    qr = Image.open(buf).convert("RGB")
    x = left + logo.width + 150
    top = (SIZE[1] - qr.height - 110) // 2        # the code and its two lines, centred
    card.paste(qr, (x, top))

    pen = ImageDraw.Draw(card)
    big = ImageFont.truetype(str(FONT), 30)
    small = ImageFont.truetype(str(FONT), 22)
    pen.text((x, top + qr.height + 30), shown(url), font=big, fill=TEXT)
    pen.text((x, top + qr.height + 76), "personal research · not financial advice", font=small, fill=MUTED)
    return card


def save(url: str) -> None:
    """Write the card with its address stored inside."""
    from PIL.PngImagePlugin import PngInfo

    info = PngInfo()
    info.add_text(KEY, url)
    draw(url).save(CARD, pnginfo=info, optimize=True)


def stored_address(path: Path) -> str | None:
    """The `address` text chunk of a PNG, read without an image library."""
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    pos = 8
    while pos + 8 <= len(data):
        length, kind = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + length]
        if kind == b"tEXt" and b"\x00" in body:
            name, value = body.split(b"\x00", 1)
            if name.decode("latin-1") == KEY:
                return value.decode("latin-1")
        if kind == b"zTXt" and b"\x00" in body:
            name, rest = body.split(b"\x00", 1)
            if name.decode("latin-1") == KEY:
                return zlib.decompress(rest[1:]).decode("latin-1")
        pos += 12 + length
    return None


def stale() -> list[str]:
    """The card, when it is missing or carries another address."""
    if not CARD.is_file() or stored_address(CARD) != build_qr.page_url():
        return [str(CARD.relative_to(ROOT))]
    return []


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    p.add_argument("--check", action="store_true", help="compare only, write nothing")
    args = p.parse_args(argv)
    url = build_qr.page_url()
    if args.check:
        bad = stale()
        for name in bad:
            print(f"❌ {name}: does not carry {url} — run python3 scripts/build_card.py")
        return 1 if bad else 0
    save(url)
    print(f"✅ assets/card.png — {shown(url)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
