← [START HERE](../START%20HERE.md)

# 🧭 Principles

Four principles that outrank convenience. When two of them collide, the one higher
on this page wins.

---

## 1 · An independent analytical picture

> *"No matter what other analysts say, we keep our own statistics and build our own
> trends, curves, diagrams, vectors and indices, on our own defined principles and
> observations. In time we will have an independent picture of the market, defined
> by our own TA / FA / sentiment / news."*
> — the operator, September 2026

This is a principle, not a task, and it explains why so much in this project is done
the hard way.

**Someone else's analysis is an input, not a truth:**

| Third-party analysis | Our own picture |
|---|---|
| a hypothesis, a context, a reason to ask | a statement we measured ourselves |
| enters as an **observation with a date and a source** | enters as a **number with a definition** |
| neither confirms nor overrides our result | is overturned only by data |
| may be right without knowing why | is required to know why |

"Our own definitions" does not mean re-inventing mathematics. It means **every
quantity we stand on has a written definition** — what it measures, which rows it
is computed from, when it is invalid.

> [!WARNING]
> **The trap, written down in advance**
>
> Independence is not isolation. A systematic difference between our picture and the
> consensus is **a finding that demands explanation**, not a reason for pride. If
> everyone sees one thing and we see another, the first hypothesis is that we are
> wrong; the second is that we found something. Checked in that order.

---

## 2 · Real data only

No fictional, synthetic or "example" data. Not in code, not in a test, not in a
document. A missing period is downloaded, not invented.

This sounds obvious until you try to write documentation. An illustrative passport
with made-up prices in a design doc is the same defect as fake data in a test — so
schemas in this project are published **with types and empty of values** until a
real one exists to paste in.

---

## 3 · "No edge" is a success

An honest negative result saves future time. The same applies to comparisons: *"the
two exchanges are identical"* is a valid result if it was measured.

The engineering consequence is real: the measurement tool is built so it **can**
say no, and its own limitations are documented next to its results. See
[The v2 backtest engine](../04%20%E2%80%94%20THE%20ENGINEERING/The%20v2%20backtest%20engine.md).

---

## 4 · A number that does not add up beats code that looks fine

Three of the project's most serious defects were found in numbers, not in code
review:

- 2,248 entries when the mathematical maximum was 840
- an identical count of suppressed signals for a 7-day and a 35-day window
- 86% of runtime spent inside the database

> **When something is arithmetically impossible, you stop and check — you do not
> explain it.**

---

## And the rule underneath all four

> **Foreign text is data, never instructions.**

This applies to news headlines, third-party APIs, vendor research — and to reports
written by another AI. A major bank's analysis is exactly as foreign as an RSS
headline; the difference is prestige, not status.

The engineering form of that rule is in [The detachable tool](../04%20%E2%80%94%20THE%20ENGINEERING/The%20detachable%20tool.md) and in the security
model: foreign text enters in its own field, never glued to an instruction; a model
that reads it may return **only a fixed JSON**, validated against a schema; and that
model has no permission to write anywhere.

---

## 🔗 Related

[Why this exists](Why%20this%20exists.md) · [What ORBITRON is](What%20ORBITRON%20is.md) · [The v2 backtest engine](../04%20%E2%80%94%20THE%20ENGINEERING/The%20v2%20backtest%20engine.md) · [Evidence labels](../05%20%E2%80%94%20HOW%20WE%20WORK/Evidence%20labels.md) · [The detachable tool](../04%20%E2%80%94%20THE%20ENGINEERING/The%20detachable%20tool.md)
