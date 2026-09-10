← [START HERE](START%20HERE.md)

# 🔤 Glossary

The project's own vocabulary. Each of these exists because a nameless thing turned
out to be hard to measure or easy to confuse.

---

## The chain

| Term | Meaning |
|---|---|
| **the press** *(the slot)* | the one fixed machine that takes any pattern and produces records in one format → [The tomato press](03%20%E2%80%94%20THE%20SYSTEM/The%20tomato%20press.md) |
| **slot position** | how many patterns run at once — currently three. Not a technical limit |
| **pattern** | a rule that marks moments in a candle series. Deliberately not called a "template" or a "model" |
| **passport** | a module's declaration of its inputs, outputs, version, compatibility and status |
| **signal** | one marked moment: which pattern, when, direction, price, strength |
| **the glue** | the ~50-line freqtrade strategy file that asks the core a question and passes the answer along. Contains no conditionals |
| **the head / the hand** | the head decides (ours), the hand executes (freqtrade) → [The head and the hand](03%20%E2%80%94%20THE%20SYSTEM/The%20head%20and%20the%20hand.md) |

## The engine

| Term | Meaning |
|---|---|
| **STRATEGY ENGINE** | the four stages between a bare signal and a live trade → [STRATEGY ENGINE](04%20%E2%80%94%20THE%20ENGINEERING/STRATEGY%20ENGINE.md) |
| 🛰️ **lost in space** | stage 1 — a bare technical signal |
| 🏠 **found home** | stage 2 — the signal dressed in the day's context |
| 🎓 **back to school** | stage 3 — *trade or not, and what kind*. The most critical environment |
| 🔥 **in fire** | stage 4 — the trade at the exchange |
| **hard block** | a state that forbids a direction outright, with a reason. Deliberately **not** called a veto, because that word already means a dashboard button that was designed and then removed |
| **lever** | one of the four mechanisms at stage 3 — gate, multiplier, stop-tightener, tax |
| **decision passport** | the JSON contract from stage 3 to freqtrade. Distinct from a *pattern* passport — always say which |
| **detachable** | a third-party tool that can be removed without the project stopping → [The detachable tool](04%20%E2%80%94%20THE%20ENGINEERING/The%20detachable%20tool.md) |

## Research and data

| Term | Meaning |
|---|---|
| **edge** | how far a pattern's result sits above the market backdrop, after costs |
| **the baseline** | non-overlapping random windows — "what the market does on its own" |
| **declustering** | keeping the first signal of a burst, so one move is counted once |
| **the v2 engine** | the honest backtest instrument → [The v2 backtest engine](04%20%E2%80%94%20THE%20ENGINEERING/The%20v2%20backtest%20engine.md). Distinct from the *strategy* engine |
| **market backdrop** | the return of a random entry on the same day. Always printed next to a pattern's result |
| **muted** | a signal suppressed by cooldown. Kept in the database forever, collapsed to one line in the journal |
| **the golden archive** | the permanently kept daily files → [The golden archive](02%20%E2%80%94%20THE%20RESEARCH/The%20golden%20archive.md) |
| `daily info & smart money track` | the one section of the daily file that code does not write |
| **regime** | the macro state — growth × inflation. Never called a "mode" |
| **the risk axis** | risk-on / risk-off as a continuous score, not a threshold |
| **borderline month** | when two macro definitions disagree: no regime is asserted. A value, not a gap |

## Working method

| Term | Meaning |
|---|---|
| **evidence label** | ✅ verified · 🟡 claimed · ⚫ unknown → [Evidence labels](05%20%E2%80%94%20HOW%20WE%20WORK/Evidence%20labels.md) |
| **"what is not being claimed"** | the required closing section listing what does not exist yet |
| **the guard** | the pre-commit script that refuses a self-contradicting vault → [Guards and the generated map](05%20%E2%80%94%20HOW%20WE%20WORK/Guards%20and%20the%20generated%20map.md) |
| **the map** | the generated index of the vault. Never hand-written |

---

## Two names that look like one thing and are not

> ⚠️ **The engine.** *The v2 engine* is the backtest instrument that judges patterns.
> *The strategy engine* is the four-stage path from signal to trade. Different things,
> different pages.

> ⚠️ **The passport.** A *pattern* passport declares a pattern. A *decision* passport
> is the JSON sent to freqtrade. Always qualify which one.

Both pairs are in this glossary specifically because they were confused in practice.

---

## 🔗 Related

[START HERE](START%20HERE.md) · [Why this exists](01%20%E2%80%94%20THE%20IDEA/Why%20this%20exists.md) · [The tomato press](03%20%E2%80%94%20THE%20SYSTEM/The%20tomato%20press.md) · [STRATEGY ENGINE](04%20%E2%80%94%20THE%20ENGINEERING/STRATEGY%20ENGINE.md) · [The v2 backtest engine](04%20%E2%80%94%20THE%20ENGINEERING/The%20v2%20backtest%20engine.md)
