← [[START HERE]]

# 🔤 Glossary

The project's own vocabulary. Each of these exists because a nameless thing turned
out to be hard to measure or easy to confuse.

---

## The chain

| Term | Meaning |
|---|---|
| **the press** *(the slot)* | the one fixed machine that takes any pattern and produces records in one format → [[The tomato press]] |
| **slot position** | how many patterns run at once — currently three. Not a technical limit |
| **pattern** | a rule that marks moments in a candle series. Deliberately not called a "template" or a "model" |
| **passport** | a module's declaration of its inputs, outputs, version, compatibility and status |
| **signal** | one marked moment: which pattern, when, direction, price, strength |
| **the glue** | the ~50-line freqtrade strategy file that asks the core a question and passes the answer along. Contains no conditionals |
| **the head / the hand** | the head decides (ours), the hand executes (freqtrade) → [[The head and the hand]] |

## The engine

| Term | Meaning |
|---|---|
| **STRATEGY ENGINE** | the four stages between a bare signal and a live trade → [[STRATEGY ENGINE]] |
| 🛰️ **lost in space** | stage 1 — a bare technical signal |
| 🏠 **found home** | stage 2 — the signal dressed in the day's context |
| 🎓 **back to school** | stage 3 — *trade or not, and what kind*. The most critical environment |
| 🔥 **in fire** | stage 4 — the trade at the exchange |
| **hard block** | a state that forbids a direction outright, with a reason. Deliberately **not** called a veto, because that word already means a dashboard button that was designed and then removed |
| **lever** | one of the four mechanisms at stage 3 — gate, multiplier, stop-tightener, tax |
| **decision passport** | the JSON contract from stage 3 to freqtrade. Distinct from a *pattern* passport — always say which |
| **detachable** | a third-party tool that can be removed without the project stopping → [[The detachable tool]] |

## Research and data

| Term | Meaning |
|---|---|
| **edge** | how far a pattern's result sits above the market backdrop, after costs |
| **the baseline** | non-overlapping random windows — "what the market does on its own" |
| **declustering** | keeping the first signal of a burst, so one move is counted once |
| **the v2 engine** | the honest backtest instrument → [[The v2 backtest engine]]. Distinct from the *strategy* engine |
| **market backdrop** | the return of a random entry on the same day. Always printed next to a pattern's result |
| **muted** | a signal suppressed by cooldown. Kept in the database forever, collapsed to one line in the journal |
| **the golden archive** | the permanently kept daily files → [[The golden archive]] |
| `daily info & smart money track` | the one section of the daily file that code does not write |
| **regime** | the macro state — growth × inflation. Never called a "mode" |
| **the risk axis** | risk-on / risk-off as a continuous score, not a threshold |
| **borderline month** | when two macro definitions disagree: no regime is asserted. A value, not a gap |

## Working method

| Term | Meaning |
|---|---|
| **evidence label** | ✅ verified · 🟡 claimed · ⚫ unknown → [[Evidence labels]] |
| **"what is not being claimed"** | the required closing section listing what does not exist yet |
| **the guard** | the pre-commit script that refuses a self-contradicting vault → [[Guards and the generated map]] |
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

[[START HERE]] · [[The tomato press]] · [[STRATEGY ENGINE]] · [[The v2 backtest engine]]
