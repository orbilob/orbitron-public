← [START HERE](../START%20HERE.md)

# 📅 The daily file

Every day the system writes one Markdown file. This is what it contains and why each
part is shaped the way it is.

---

## The shape

```markdown
# ORBITRON — 2026-08-26

## 📊 The market today
Open · Close · High · Low · Range · Direction · Volume vs. the 30-day average

## 🧠 daily info & smart money track
   ← the only section code does not write

## ⚡ Strongest moves
| Hour | Direction | Move | Volume |

## 🎯 Signals
### 16:43 · A001 · LONG · SIGNAL
Conditions met: …
Follow-up: +0.6% at 60 min ✅ · +0.4% at 4h · −0.1% at 8h
Context: —

_47 suppressed by cooldown · A001 · 16:44–17:31_

## 📈 Per-pattern summary
| Pattern | Signals | Hit rate 60m | Mean result | Market backdrop |

## 🩺 System health
Candles: 1440/1440 · Missing minutes: 0 · Gaps: none
| Table | Rows | Expected | Coverage |
```

---

## Four rules the archive carries

### 1 · The market backdrop always sits next to the result

`+0.28%` means nothing if the market itself returned `+0.30%` that day. **Every
number for a pattern travels with the number for a random entry on the same day.**

This is the daily-file version of the same rule that governs the validation engine: a
metric without a baseline is advertising.

### 2 · No verdicts in the daily file

Not *"A001 is working well"*. One day is noise — the verdict comes from accumulation,
not from the evening.

### 3 · The file gets appended to, not rewritten

A signal at 22:00 gets its four-hour result the next day. The script goes back and
completes yesterday's file.

### 4 · Suppressed sequences collapse to one line

> [!WARNING]
> **Why this rule exists — with numbers from a real day**
>
> One pattern produced **139 signals**, of which **125 were suppressed** by cooldown.
> At five lines per block that is ~625 lines of noise, and the per-pattern summary
> gets buried at the bottom. A file meant to be kept forever and read by a human
> became unreadable on day two.

A full block is written only for a signal that would actually have outcomed. A run of
suppressed ones becomes a single italic sentence preserving the count, the pattern,
the time span, the reason and the score range.

> **Nothing is lost.** The suppressed signals live in the database forever and
> research reads them from there. **The journal is a reading of the database, not the
> database itself.** And the summary section still counts *all* rows, suppressed
> included.

---

## 🧠 The one section code does not write

`daily info & smart money track` is **manual**, and it sits immediately after "the
market today".

> [!CAUTION]
> **It is written once and never regenerated**
>
> The daily report can regenerate the last few days. If the human summary were
> produced at generation time, the text from the 19th would quietly become today's
> reading of that day — and an archive that "cannot be reconstructed after the fact"
> would begin rewriting itself.
>
> Because it comes from a separate file, regeneration returns the same text verbatim.

**A day with no written text shows a dash.** The blank is the honest answer — better
than code inventing a sentence that nobody can distinguish from an observation a
year later.

---

## 🩺 And two notes on honesty in the health section

**"I'm breathing" is not "I'm working".** A heartbeat is sent while the process is
alive — but the collector can be alive, the venue returning errors, and nothing
entering the database. Then monitoring reports calm while there is no data. So: ping
only if the **row count increased**.

**The heartbeat does not write to the database.** The health line says what is
actually known, rather than defaulting to "uninterrupted".

---

## 🔗 Related

[Why this exists](../01%20%E2%80%94%20THE%20IDEA/Why%20this%20exists.md) · [The golden archive](The%20golden%20archive.md) · [Smart money track](Smart%20money%20track.md) · [Market regimes](Market%20regimes.md) · [The chain](../03%20%E2%80%94%20THE%20SYSTEM/The%20chain.md)
