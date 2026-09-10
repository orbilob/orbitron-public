← [START HERE](START%20HERE.md)

# 🔤 Glossary

The project's own vocabulary. Each of these exists because a nameless thing turned
out to be hard to measure or easy to confuse.

---

## Observation

| Term | Meaning |
|---|---|
| **the press** *(the slot)* | the one fixed machine that takes any pattern and produces records in one format → [The tomato press](03%20%E2%80%94%20THE%20SYSTEM/The%20tomato%20press.md) |
| **slot position** | how many patterns run at once — currently three. Not a technical limit |
| **pattern** | a rule that marks moments in a candle series. Deliberately not called a "template" or a "model" |
| **passport** | a module's declaration of its inputs, outputs, version, compatibility and status |
| **signal** | one marked moment: which pattern, when, direction, price, strength |
| **the collector** | the component that fetches from outside and computes nothing |

## The record

| Term | Meaning |
|---|---|
| **the written day** | one Markdown file per day, recording what the market did and what the world looked like while it did it |
| **the golden archive** | those files, kept permanently → [The golden archive](02%20%E2%80%94%20THE%20RESEARCH/The%20golden%20archive.md) |
| `daily info & smart money track` | the one section of the written day that code does not write |
| **market backdrop** | what a random moment on the same day returned. Always printed next to any pattern's number |
| **muted** | an observation suppressed by cooldown. Kept in the database forever, collapsed to one line in the journal |
| **forward-fill** | a value enters a day only if it was publicly known by the end of that day. Missing values carry forward, never backward |

## Measurement

| Term | Meaning |
|---|---|
| **the v2 validation engine** | the honest measuring instrument → [The v2 validation engine](04%20%E2%80%94%20THE%20ENGINEERING/The%20v2%20validation%20engine.md) |
| **edge** | how far a pattern's result sits above the market backdrop, after costs |
| **the baseline** | non-overlapping random windows — "what the market does on its own" |
| **declustering** | keeping the first observation of a burst, so one move is counted once |
| **"no edge"** | a valid and welcome answer. An honest negative result saves future time |
| **p-adjusted** | the significance value after correcting for asking many questions at once. The one that counts |

## Context

| Term | Meaning |
|---|---|
| **regime** | the macro state — growth × inflation. Never called a "mode" |
| **the risk axis** | risk-on / risk-off as a continuous score, not a threshold |
| **borderline month** | when two macro definitions disagree: no regime is asserted. A value, not a gap |
| **smart money track** | where capital goes when it leaves somewhere else → [Smart money track](02%20%E2%80%94%20THE%20RESEARCH/Smart%20money%20track.md) |

## Working method

| Term | Meaning |
|---|---|
| **evidence label** | ✅ verified · 🟡 claimed · ⚫ unknown → [Evidence labels](05%20%E2%80%94%20HOW%20WE%20WORK/Evidence%20labels.md) |
| **"what is not being claimed"** | the required closing section listing what does not exist yet |
| **the guard** | the script that refuses a self-contradicting vault → [Guards and the generated map](05%20%E2%80%94%20HOW%20WE%20WORK/Guards%20and%20the%20generated%20map.md) |
| **the map** | the generated index of the vault. Never hand-written |
| **the operator** | the person. Every decision is theirs, without exception |

---

## Two names that look like one thing and are not

> [!WARNING]
> **The passport.** A *pattern* passport declares what a pattern is and what state it
> is in. A *record* passport declares what was observed and under what conditions.
> Always qualify which one.

> [!WARNING]
> **The press and the engine.** The *press* produces records in one format. The
> *validation engine* judges whether a pattern in those records means anything.
> Different jobs, different pages.

Both pairs are here specifically because they were confused in practice.

---

## 🔗 Related

[START HERE](START%20HERE.md) · [Why this exists](01%20%E2%80%94%20THE%20IDEA/Why%20this%20exists.md) · [The tomato press](03%20%E2%80%94%20THE%20SYSTEM/The%20tomato%20press.md) · [The v2 validation engine](04%20%E2%80%94%20THE%20ENGINEERING/The%20v2%20validation%20engine.md)
