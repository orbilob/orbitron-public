← [START HERE](../START%20HERE.md)

# 🔬 The v2 backtest engine

> [!NOTE]
> **The instrument that decides whether a pattern is worth anything**
>
> Everything in the research lab rests on its verdict. This page explains what it
> does and why, assuming no prior knowledge.

---

## The one question it answers

> **"When the pattern says SIGNAL, does something better happen afterwards than if I
> had entered at a random moment?"**

Not "does it win". Not "how often is it right". But **is it better than chance** —
and by enough that it is not luck.

That is the engine's entire job.

---

## What it receives

A table of candles and one column marking which moments the pattern flagged:

```
timestamp   close     level
--------------------------------
12:00       67_100    NORMAL
12:01       67_150    NORMAL
12:02       67_090    SIGNAL     ← here the pattern says "enter"
12:03       67_200    NORMAL
```

The engine does not know and does not care **how** the pattern decided. Only where
it says `SIGNAL`. That is why a new pattern plugs in without touching the engine.

---

## Step 1 — declustering (this is where v1 was broken)

```python
kept = [signal_idx[0]]
for i in signal_idx[1:]:
    if i - kept[-1] >= min_gap:
        kept.append(i)
```

**The problem:** during a crash the pattern fires `SIGNAL` on every candle — say
twenty in a row. Those are not twenty opportunities. That is **one** move, seen
twenty times.

> Like filming one goal with twenty cameras and then counting twenty goals.

Why it is fatal: statistics asks "how many independent observations do you have". Tell
it twenty instead of one and it becomes twenty times more confident than it has any
right to be.

**The fix:** from each cluster of nearby signals, keep the **first** — the moment you
would actually have entered.

> [!NOTE]
> **Why the first and not the strongest**
>
> A historical scan keeps the strongest, because there you are looking back and
> asking which move was most pronounced. Here you keep the first, because you are
> simulating trading: in the real moment you do not know whether it will get stronger
> five minutes later.

---

## Step 2 — costs, deducted before the test

```python
returns = returns - self.cost      # fee + slippage
```

Costs come out **before** the test, not after. This is where most "profitable"
strategies die — their edge is smaller than the price of capturing it.

> [!WARNING]
> **The baseline deliberately does NOT pay costs**
>
> The comment in the code is exact: *"what would have happened without me"*. You
> compare a real trade with costs against the market backdrop without costs. Harsh
> towards yourself — the correct direction for strictness.
>
> The price of that choice: `edge` is no longer a purely statistical quantity but an
> economic one. Defensible, but worth knowing. **The engine documents its own
> compromises next to its results.**

---

## Step 3 — the baseline

```python
base_idx = np.arange(0, n - horizon, horizon)
```

Windows taken exactly `horizon` bars apart — that is, **non-overlapping**. 0–24,
24–48, 48–72.

v1 took every possible window: 0–24, 1–25, 2–26… Adjacent windows shared 23 of their
24 hours. The same mistake again — one move counted many times.

This is "what the market does on its own". If your pattern does not beat that
number, it contributes nothing.

---

## Step 4 — the t-test

```python
t_stat, p_value = stats.ttest_ind(returns, base_returns, equal_var=False)
```

The test answers: **"if there were no real difference between the two groups, how
often would chance alone produce a difference at least this large?"**

That answer is `p`. `equal_var=False` means equal spread is not assumed — the more
cautious variant.

> [!TIP]
> **Why everything before this mattered**
>
> The t-test **believes** what you hand it. Tell it 500 observations and it computes
> with 500. If those 500 are really 25 events counted twenty times each, it computes
> a confidence it has no basis for. Steps 1 and 3 exist for the sole purpose of not
> lying to it.

---

## Step 5 — Benjamini-Hochberg correction

```python
adj = min(prev, p_value * m / rank)
```

**The problem:** you test four horizons at once. At a 0.05 threshold each has a 5%
chance of fooling you. Across four tests, the chance that *at least one* fools you
is roughly 18%, not 5%.

> Flip twenty coins ten times each — one of them will look suspiciously good, for no
> reason at all.

**The fix:** sort the p-values and raise the bar for each according to its rank. The
result is `p_adjusted`, and that is the number that means something.

---

## When a result counts as a finding

```python
h.significant = bool(h.p_adjusted < self.alpha and h.edge > 0)
```

**Both** conditions, simultaneously:

1. `p_adjusted < 0.05` — not chance
2. `edge > 0` — better than the market

The second is not redundant. You can get a strongly significant result saying the
pattern is **systematically worse** than the baseline. That has actually happened —
a continuation hypothesis came back significant and negative.

---

## Reading the report

```
Hor      N   Base    Win%    AvgRet      Edge   R/Risk        p    p_adj
4     1459   3421   63.3%     0.32%    +0.30%    0.089    0.000    0.000  ✅
8     1187   1710   61.0%     0.36%    +0.36%    0.077    0.000    0.000  ✅
24     452    570   54.1%     0.11%    +0.05%    0.012    0.041    0.082  ⚠️
```

| Column | Meaning |
|---|---|
| `N` | signals **after** declustering — the real sample size |
| `Base` | count of non-overlapping baseline windows |
| `AvgRet` | mean return **after** costs |
| `Edge` | how far above the market backdrop — **this is the number** |
| `R/Risk` | return / dispersion. It is not a Sharpe ratio and is deliberately not called one |
| `p_adj` | after correction — **this is the one you read** |

- ✅ passes even after correction. A finding.
- ⚠️ raw `p` passes, corrected does not. **Does not count.**

---

## Built-in defences

- **`min_signals = 30`** — under thirty independent signals, a warning is printed. It
  does not block, but it makes you think.
- **`ddof=1`** — sample standard deviation, not population. The correct one when you
  are measuring a sample.
- **Signals too close to the end are discarded** — otherwise the last trades would be
  measured against incomplete windows.

---

## What the engine does NOT do

Worth being explicit, because it is easy to expect more:

- **It does not model exits.** It closes at a fixed horizon. No stop, no trailing, no
  "get out early".
- **It does not check normality.** The t-test assumes a reasonable distribution; crypto
  returns have fat tails. Next step: a permutation test or block bootstrap.
- **It does not know about regimes.** A bull market and a bear market are computed
  together.
- **It is not calibrated, it is cautious.** Its corrected error rates sit *below* the
  nominal 5%. Which means **"no edge" from this engine does not prove there is none.**

---

## ⭐ The story that justifies the whole rebuild

The first version of this engine found "edge" in **44% of cases on pure noise**.

A pattern had been marked *validated* by it. When the corrected engine was built, that
pattern was re-run: **zero edge**, and on longer horizons significantly *worse* than
the baseline. The "proven edge" had been entirely an artifact of the broken
instrument.

> The lesson was not "the pattern was too complex". It was: **the measuring
> instrument was lying, and it was lying for both of them.**

That is why a negative result is treated as a success here, and why the engine's own
limitations are documented on the same page as its findings.

---

## In one sentence

> The engine counts every move once, compares it to the market, pays the costs,
> raises the bar for testing many things at once — and only then says "this is a
> finding".

Boring. That is exactly why it works.

---

## 🔗 Related

[Why this exists](../01%20%E2%80%94%20THE%20IDEA/Why%20this%20exists.md) · [Principles](../01%20%E2%80%94%20THE%20IDEA/Principles.md) · [The tomato press](../03%20%E2%80%94%20THE%20SYSTEM/The%20tomato%20press.md) · [Repositories](Repositories.md) · [The detachable tool](The%20detachable%20tool.md)
