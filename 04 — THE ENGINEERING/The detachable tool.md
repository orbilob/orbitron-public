← [START HERE](../START%20HERE.md)

# 🔌 The detachable tool

> [!TIP]
> **The decision**
>
> **The authored environment is not mixed with third-party software. We use tools —
> but every one of them detaches at any moment.**

Third-party software enters the project **only as a tool that can leave.** No foreign
component is load-bearing.

---

## The test, deliberately crude

> ### Remove the tool in your head. If the project stops working, it was not a tool but a foundation — and the rule is broken.

That is the whole check. It takes ten seconds and it is remarkably hard to argue
your way around.

---

## What "detaches" means

Not "if we really have to, we'll pull it out". It means **by construction, at any
moment**:

| Condition | How it is met |
|---|---|
| **The boundary is a format, not a call** | the engine's output is JSON. A different hand = a different reader of the same JSON |
| **Ours imports nothing from theirs** | the core imports nothing from freqtrade — a legal boundary (GPL-3.0) and an architectural one at once |
| **Theirs holds none of our data** | the truth lives in our own database and in the daily file, not in the tool's storage |
| **Theirs holds none of our logic** | the glue is ~50 lines with **not one conditional inside** ✅ verified |

That last row is the one that can be checked mechanically, which is why it is stated
as a line count rather than an intention.

---

## Where it applies today — two places

| Place | The tool | Its role |
|---|---|---|
| 🎯 **Stage 4 · in fire** | **freqtrade** | the hand: sending, the exchange-side stop, monitoring |
| 🧪 **The research lab** | **freqtrade's backtest engine** | an instrument in backtesting |

The second one is the interesting case, because it is where the rule almost broke.
The lab is described as *"powered by freqtrade backtest engine"* — and that phrasing
is deliberate: powered by, not built on.

> [!CAUTION]
> **The boundary this forces in the lab**
>
> freqtrade's backtester **does not replace the v2 engine** and does not become
> the measure of truth.
>
> It answers *"what would this rule have done"*. The v2 engine answers *"is there an
> edge at all"* — with declustering, a non-overlapping baseline, costs deducted first
> and a multiple-testing correction. The third-party one does none of that.
>
> **The order is not reversible: v2 first, then freqtrade's backtester.**
>
> A tool that starts deciding what counts as a finding is no longer detachable —
> it has become methodology.

---

## Why this rule is worth its cost

**It is not about distrust of a specific project.** It is about what happens over
years:

- A dependency that holds your data holds your exit cost.
- A dependency that holds your logic holds your understanding.
- A dependency that defines your success metric holds your research direction.

The first is annoying, the second is expensive, and the third is the one that ends
projects quietly — you stop asking questions the tool cannot answer.

## And the cheapest way to enforce it

Express the boundary as a **format**. Then detachability is not a promise made in a
design review; it is a file you can open.

---

## 🔗 Related

[The head and the hand](../03%20%E2%80%94%20THE%20SYSTEM/The%20head%20and%20the%20hand.md) · [STRATEGY ENGINE](STRATEGY%20ENGINE.md) · [Contracts and formats](Contracts%20and%20formats.md) · [The v2 backtest engine](The%20v2%20backtest%20engine.md)
