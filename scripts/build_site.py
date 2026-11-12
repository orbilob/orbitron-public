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
import hashlib
import html.parser
import json
import re
import shutil
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "_site"
PAGE = SITE / "index.html"
BULGARIAN = SITE / "i18n" / "bg.json"
LINKS = SITE / "links.json"
DATA = ("board", "chain", "patterns")
DAYS = ROOT / "days"

# ---------------------------------------------------------------- the daily report
# One file per day, days/YYYY-MM-DD.json, format `public_day` 1.0 — the
# contract is written in the private vault (FORMATS) and decided in D20:
# words written by hand in two languages, the day's scheduled events, and
# nothing else. No prices and no number from any data vendor: the free data
# plans the project uses do not allow showing their data to anyone, and the
# operator decided on 12.11.2026 that the report carries no numbers at all.
#
# The shape is pinned by a fingerprint. ORCORE, which prints the events of a
# day from its calendar in this shape, pins the same one — change the shape
# on one side alone and that side turns red (vault R-COMPAT).
DAY_FORMAT, DAY_VERSION = "public_day", "1.0"
DAY_KEYS = ("day", "events", "format", "version", "words")
EVENT_KEYS = ("country", "name", "time")
WORD_KEYS = ("bg", "en")
DAY_SHAPE = (f"{DAY_FORMAT} {DAY_VERSION} | {' '.join(DAY_KEYS)} | "
             f"events: {' '.join(EVENT_KEYS)} | words: {' '.join(WORD_KEYS)}")
DAY_FINGERPRINT = "b9293fcd094949c4"
WORDS_MAX = 1500

# Words that turn a description of a day into advice. Not the withheld
# vocabulary (that is D13's); these are the report's own rule: it describes
# a day, it never says what to do.
ADVICE = {
    r"\b(?:buy|sell) now\b": "advice",
    r"\bshould (?:buy|sell)\b": "advice",
    r"\bgo(?:ing)? (?:long|short)\b": "advice",
    r"\b(?:long|short) (?:position|entry)\b": "advice",
    r"\bentry point\b": "advice",
    r"\btake[- ]profit\b": "advice",
    r"\bstop[- ]loss\b": "advice",
    r"\bprice target\b": "advice",
    r"\brecommend\w*": "advice",
    r"\bguarantee\w*": "advice",
    r"\bкупете\b|\bкупувайте\b": "advice",
    r"\bпродайте\b|\bпродавайте\b": "advice",
    r"\bлонг\w*|\bшорт\w*": "advice",
    r"\bпрепоръч\w*": "advice",
    r"\bгарантира\w*": "advice",
    r"\bцелева цена\b": "advice",
    r"\bстоп[- ]лос\w*|\bтейк[- ]профит\w*": "advice",
}

# No numbers in the words: no currency, no percent, no decimals, nothing of
# three digits or more. A clock time (13:30) and a small count pass.
NUMBERS = {
    r"[%$€£]": "a currency or a percent",
    r"\d+[.,]\d+": "a decimal or a grouped number",
    r"\d{3,}": "a number of three digits or more",
    r"\d\s*(?:bp|bps|pp)\b": "basis points",
}
TIME = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
COUNTRY = re.compile(r"^[A-Z]{2,3}$")

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
    """Every translation key on the page, with the English text it stands for.

    A key may appear more than once — a tile and its panel share a label — but
    then it must say the same thing every time, or one key would stand for two
    texts and the Bulgarian could match only one of them.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.english: dict[str, str] = {}
        self.twice: list[str] = []                    # keys with two different English texts
        self._open: list[tuple[str, str, list[str]]] = []   # (tag, key, text so far)

    def _record(self, key: str, text: str) -> None:
        text = " ".join(text.split())
        if key in self.english and self.english[key] != text:
            self.twice.append(key)
        self.english.setdefault(key, text)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        found = dict(attrs)
        for attr, source in (("data-i18n-content", "content"), ("data-i18n-alt", "alt"),
                             ("data-i18n-aria", "aria-label")):
            if found.get(attr):
                self._record(found[attr], found.get(source) or "")
        if found.get("data-i18n"):
            self._open.append((tag, found["data-i18n"], []))

    def handle_data(self, data: str) -> None:
        if self._open:
            self._open[-1][2].append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._open and self._open[-1][0] == tag:
            _, key, parts = self._open.pop()
            self._record(key, "".join(parts))


def english_keys() -> tuple[dict[str, str], list[str]]:
    """The page's English by key, and the keys that say two different things."""
    parser = _Keys()
    parser.feed(PAGE.read_text(encoding="utf-8"))
    return parser.english, sorted(set(parser.twice))


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

    english, twice = english_keys()
    for key in twice:
        findings.append(f"site/index.html: \"{key}\" stands for two different English texts")
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

    # 4 — a stylesheet whose comments do not pair up. A stray "*/" leaves the
    #     text after it outside any comment, the browser reads it as a selector
    #     and drops the rule that follows — on 12.11.2026 that rule was the
    #     whole dark theme, and no other check noticed.
    for path in sorted(SITE.rglob("*.css")):
        text = path.read_text(encoding="utf-8")
        opened, closed = text.count("/*"), text.count("*/")
        if opened != closed:
            findings.append(
                f"{path.relative_to(ROOT)}: {opened} comment(s) opened, {closed} closed — "
                "the text between them is read as CSS"
            )

    # 5 — the daily report: the pinned shape, then every day
    if day_fingerprint() != DAY_FINGERPRINT:
        findings.append(f"scripts/build_site.py: the day format's shape changed — fingerprint "
                        f"{day_fingerprint()}, pinned {DAY_FINGERPRINT}. Change the pin here, in "
                        f"ORCORE and in the vault's FORMATS in one go")
    for path, card in read_days():
        findings.extend(check_day(path, card, rules))

    # 6 — the links the page offers to follow the project
    try:
        links = json.loads(LINKS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return findings + [f"site/links.json: not readable as JSON — {e}"]
    for link in links.get("follow", []):
        if not str(link.get("url", "")).startswith("https://"):
            findings.append(f"site/links.json: \"{link.get('name')}\" is not an https:// address")

    return findings


def day_fingerprint() -> str:
    return hashlib.sha256(DAY_SHAPE.encode("utf-8")).hexdigest()[:16]


def read_days() -> list[tuple[Path, object]]:
    """Every day file with what it parses to — or the error it raised."""
    if not DAYS.is_dir():
        return []
    out: list[tuple[Path, object]] = []
    for path in sorted(DAYS.glob("*.json")):
        try:
            out.append((path, json.loads(path.read_text(encoding="utf-8"))))
        except (OSError, json.JSONDecodeError) as e:
            out.append((path, e))
    return out


def check_day(path: Path, card: object, rules: dict[str, str],
              today: date | None = None) -> list[str]:
    """Everything wrong with one day of the report, one line each."""
    where = path.relative_to(ROOT)
    if isinstance(card, Exception):
        return [f"{where}: not readable as JSON — {card}"]
    if not isinstance(card, dict) or tuple(sorted(card)) != DAY_KEYS:
        keys = sorted(card) if isinstance(card, dict) else type(card).__name__
        return [f"{where}: the keys are {keys}, the format says {list(DAY_KEYS)}"]
    out: list[str] = []
    if card["format"] != DAY_FORMAT or card["version"] != DAY_VERSION:
        out.append(f"{where}: format {card['format']!r} {card['version']!r}, "
                   f"expected {DAY_FORMAT!r} {DAY_VERSION!r}")
    try:
        day = date.fromisoformat(str(card["day"]))
    except ValueError:
        return out + [f"{where}: day {card['day']!r} is not a date"]
    if path.stem != day.isoformat():
        out.append(f"{where}: the file is named for {path.stem}, the card says {day}")
    if day > (today or datetime.now(timezone.utc).date()):
        out.append(f"{where}: {day} has not happened yet")

    events = card["events"]
    if not isinstance(events, list):
        out.append(f"{where}: events is not a list")
        events = []
    for n, e in enumerate(events, start=1):
        if not isinstance(e, dict) or tuple(sorted(e)) != EVENT_KEYS:
            out.append(f"{where}: event {n} has keys {sorted(e) if isinstance(e, dict) else e!r}, "
                       f"the format says {list(EVENT_KEYS)}")
            continue
        if not TIME.match(str(e["time"])):
            out.append(f"{where}: event {n} time {e['time']!r} is not HH:MM")
        if not COUNTRY.match(str(e["country"])):
            out.append(f"{where}: event {n} country {e['country']!r} is not a code")
        if not str(e["name"]).strip() or len(str(e["name"])) > 80:
            out.append(f"{where}: event {n} name is empty or longer than 80")

    words = card["words"]
    if not isinstance(words, dict) or tuple(sorted(words)) != WORD_KEYS:
        out.append(f"{where}: words carry {sorted(words) if isinstance(words, dict) else words!r}, "
                   f"the format says {list(WORD_KEYS)}")
        words = {}
    for lang, text in words.items():
        text = str(text)
        if not text.strip():
            out.append(f"{where}: the words in {lang} are empty — a day is published written, or not at all")
        if len(text) > WORDS_MAX:
            out.append(f"{where}: the words in {lang} are {len(text)} characters, the most is {WORDS_MAX}")
        for pattern, why in {**ADVICE, **NUMBERS}.items():
            for match in re.finditer(pattern, text, re.IGNORECASE):
                out.append(f"{where}: words {lang} — \"{match.group(0)}\" is {why}")

    text = path.read_text(encoding="utf-8")
    for pattern, why in rules.items():
        for match in re.finditer(pattern, text, re.IGNORECASE):
            out.append(f"{where}: withheld word \"{match.group(0)}\" — {why}")
    return out


def days_for_site() -> dict:
    """The published days, newest first, each with its edition number."""
    cards = [card for _, card in read_days() if isinstance(card, dict)]
    cards.sort(key=lambda c: c["day"])
    for n, card in enumerate(cards, start=1):
        card["edition"] = n
    return {"days": list(reversed(cards))}


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
    (OUT / "data" / "days.json").write_text(json.dumps(days_for_site(), ensure_ascii=False, indent=2) + "\n",
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
