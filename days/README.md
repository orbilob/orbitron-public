# The daily report — one file per day

`days/YYYY-MM-DD.json`, format **`public_day` 1.0**. The page shows the newest
as the *ORBITRON Daily Report*; each file is one edition, numbered by date.

```json
{
  "format": "public_day",
  "version": "1.0",
  "day": "YYYY-MM-DD",
  "events": [{ "time": "HH:MM", "country": "US", "name": "the event, as the calendar names it" }],
  "words": { "en": "the day, in words", "bg": "денят с думи" }
}
```

**What a day carries — and what it never does.** Words written by hand in two
languages, approved by the author, and the day's scheduled three-star events
(time in UTC, country, name). No prices, no number from any data vendor, no
forecast and no advice. `scripts/build_site.py` refuses a day that breaks any
of this: a missing or extra key, a date that is not the file's name or has not
happened yet, empty words, a currency or percent sign, a decimal or a number of
three digits or more, an advice phrase, the withheld vocabulary — in English
and in Bulgarian.

**Published once and kept.** A day is written, approved and merged; it is not
rewritten afterwards. The edition number is its place in the dated list.

**Where the events come from.** The project's own calendar; the private
repository prints a day's events in exactly this shape, and both sides pin the
shape with the same fingerprint, so neither can change it alone.
