#!/usr/bin/env python3
"""Assemble the public page, and refuse it when it would say something it must not.

Why a build step at all: the page reads board.json, chain.json and patterns.json —
the same three files the README is drawn from. Copying them into the site by hand
would make a second copy that drifts on the next export. So the site is ASSEMBLED
from the repository on every deploy, and the data has one home: the root.

Why the checks live here and run from check_vault.py: the page is the most visible
thing the project publishes, and the only one in two languages. A guard that reads
only Markdown would let the page leak in Bulgarian what the vault refuses in
English. So the page is held to the same withheld vocabulary — in both languages —
and to one more rule of its own: every piece of English text has a Bulgarian line,
and every Bulgarian line answers to a piece of English text. A translation that
quietly falls behind is a page that tells two audiences two different things.

English lives once, in site/index.html. Bulgarian lives once, in site/i18n/bg.json.

Run from the vault root:   python3 scripts/build_site.py           # build into _site/
                           python3 scripts/build_site.py --check   # checks only
"""

from __future__ import annotations

import ast
import html.parser
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "_site"
PAGE = SITE / "index.html"
BULGARIAN = SITE / "i18n" / "bg.json"
LINKS = SITE / "links.json"
DATA = ("board", "chain", "patterns")

# The same two families check_vault.py withholds in English, in Bulgarian.
# Decided on 12.11.2026 together with the language switch: a page in two
# languages is guarded in two languages, or the switch is a way around the guard.
WITHHELD_BG = {
    r"api[- ]?ключ\w*": "names a credential",
    r"частн\w* ключ\w*": "names a credential",
    r"тайн?\w* ключ\w*": "names a credential",
    r"токен\w* за достъп": "names a credential",
    r"\bпарол\w*": "names a credential",
    r"\bпортфейл\w*": "names a credential store",
    r"\bтъргов\w*": "execution vocabulary",
    r"\bсделк\w*": "execution vocabulary",
    r"\bборс\w*": "execution vocabulary",
    r"\bливъридж\w*": "execution vocabulary",
    r"\bлостов\w* ефект\w*": "execution vocabulary",
    r"\bскалп\w*": "execution vocabulary",
    r"\bброкер\w*": "execution vocabulary",
    r"книга(та)? на поръчките": "execution vocabulary",
}

# The files of the page that carry words a reader can see or a crawler can read.
TEXT_SUFFIXES = {".html", ".js", ".css", ".json"}

PLACEHOLDER = re.compile(r"\{(\w+)\}")
KEY_ATTRS = ("data-i18n", "data-i18n-content", "data-i18n-alt", "data-i18n-aria")


class _Keys(html.parser.HTMLParser):
    """Every translation key on the page, with the English text it stands for."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.english: dict[str, str] = {}
        self._open: list[tuple[str, str]] = []   # (tag, key) awaiting their text

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        found = dict(attrs)
        for attr, source in (("data-i18n-content", "content"), ("data-i18n-alt", "alt"),
                             ("data-i18n-aria", "aria-label")):
            if found.get(attr):
                self.english.setdefault(found[attr], found.get(source) or "")
        if found.get("data-i18n"):
            self._open.append((tag, found["data-i18n"]))
            self.english.setdefault(found["data-i18n"], "")

    def handle_data(self, data: str) -> None:
        if self._open:
            key = self._open[-1][1]
            self.english[key] = self.english.get(key, "") + data

    def handle_endtag(self, tag: str) -> None:
        if self._open and self._open[-1][0] == tag:
            self._open.pop()


def english_keys() -> dict[str, str]:
    parser = _Keys()
    parser.feed(PAGE.read_text(encoding="utf-8"))
    return {k: v.strip() for k, v in parser.english.items()}


def pillar_lines() -> dict[str, str]:
    """The one line under each pillar — owned by build_readme.py, which draws it too."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_readme  # noqa: E402
    return dict(build_readme.PILLAR_LINE)


def check(withheld_en: dict[str, str]) -> list[str]:
    """Everything wrong with the page, one line each. Empty means publishable."""
    findings: list[str] = []
    if not PAGE.is_file():
        return [f"{PAGE.relative_to(ROOT)}: the page is missing"]

    english = english_keys()
    try:
        bulgarian = json.loads(BULGARIAN.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return [f"{BULGARIAN.relative_to(ROOT)}: not readable as JSON — {e}"]

    chain = json.loads((ROOT / "chain.json").read_text(encoding="utf-8"))
    pillars = {f"pillar.{p['name']}" for p in chain["pillars"]} | {
        f"pillar.{name}" for name in pillar_lines()
    }

    # 1 — every English text has its Bulgarian line, and the other way round
    for key in sorted(english):
        if not str(bulgarian.get(key, "")).strip():
            findings.append(f"site/i18n/bg.json: no Bulgarian for \"{key}\"")
    for key in sorted(pillars):
        if not str(bulgarian.get(key, "")).strip():
            findings.append(f"site/i18n/bg.json: no Bulgarian line under the pillar \"{key}\"")
    for key in sorted(set(bulgarian) - set(english) - pillars):
        findings.append(f"site/i18n/bg.json: \"{key}\" answers to no text on the page")

    # 2 — a sentence that carries a number carries it in both languages
    for key, text in english.items():
        if key in bulgarian:
            ours, theirs = set(PLACEHOLDER.findall(text)), set(PLACEHOLDER.findall(str(bulgarian[key])))
            if ours != theirs:
                findings.append(
                    f"site/i18n/bg.json: \"{key}\" fills {sorted(theirs)}, the English fills {sorted(ours)}"
                )

    # 3 — the withheld vocabulary, in English and in Bulgarian, over every file of the page
    rules = {**withheld_en, **WITHHELD_BG}
    for path in sorted(SITE.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        for pattern, why in rules.items():
            for match in re.finditer(pattern, text, re.IGNORECASE):
                line = text.count("\n", 0, match.start()) + 1
                findings.append(
                    f"{path.relative_to(ROOT)}:{line}: withheld word \"{match.group(0)}\" — {why}"
                )

    # 4 — the links the page offers to follow the project
    try:
        links = json.loads(LINKS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return findings + [f"site/links.json: not readable as JSON — {e}"]
    for link in links.get("follow", []):
        if not str(link.get("url", "")).startswith("https://"):
            findings.append(f"site/links.json: \"{link.get('name')}\" is not an https:// address")

    return findings


def _image(source: Path, target: Path, width: int) -> None:
    """A web-sized copy. Without Pillow, the original — larger, never wrong."""
    try:
        from PIL import Image
    except ImportError:
        shutil.copyfile(source, target)
        return
    with Image.open(source) as im:
        if im.width > width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        im.save(target, optimize=True)


def build() -> None:
    """Assemble _site/ from site/, the three data files and the assets."""
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SITE, OUT, ignore=shutil.ignore_patterns("links.json"))
    (OUT / "data").mkdir()
    for name in DATA:
        shutil.copyfile(ROOT / f"{name}.json", OUT / "data" / f"{name}.json")
    links = json.loads(LINKS.read_text(encoding="utf-8"))
    site = {"pillar_lines": pillar_lines(), "follow": links.get("follow", [])}
    (OUT / "data" / "site.json").write_text(json.dumps(site, ensure_ascii=False, indent=2) + "\n",
                                            encoding="utf-8")
    assets = OUT / "assets"
    assets.mkdir()
    _image(ROOT / "assets" / "logo.png", assets / "logo.png", 760)
    _image(ROOT / "assets" / "signature-full.png", assets / "signature-full.png", 220)
    _image(ROOT / "assets" / "signature.png", assets / "icon.png", 96)
    shutil.copyfile(ROOT / "assets" / "social-preview.png", assets / "social-preview.png")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")


def withheld_english() -> dict[str, str]:
    """The English list. Its one home is check_vault.py; it is read from there, not copied."""
    tree = ast.parse((ROOT / "scripts" / "check_vault.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "WITHHELD" for t in node.targets
        ):
            return ast.literal_eval(node.value)
    raise SystemExit("❌ check_vault.py has no WITHHELD list — nothing to guard the page with")


def main() -> int:
    findings = check(withheld_english())
    if findings:
        for finding in findings:
            print(f"  {finding}")
        print(f"\n❌ {len(findings)} finding(s) on the page.")
        return 1
    if "--check" in sys.argv:
        print("✅ The page — every text in both languages, nothing withheld.")
        return 0
    build()
    print(f"✅ Built {OUT.relative_to(ROOT)}/ — {sum(1 for _ in OUT.rglob('*') if _.is_file())} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
