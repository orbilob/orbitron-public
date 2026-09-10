← [START HERE](../START%20HERE.md)

# 🧭 Market regimes

> [!NOTE]
> **The idea**
>
> Instead of asking *"what is the price doing"*, ask **"what regime is the market in,
> and where is money flowing"**.

The same technical state means different things under different liquidity, a
different macro backdrop, a different mood. This is the project's core principle —
*context is part of the signal* — applied at the daily scale.

---

## Two dimensions, kept separate on purpose

### 1 · Risk-on / risk-off

Is yield being sought, or shelter?

This is deliberately **not** a modifier bolted onto exposure discipline. It is a property
of the market, and it belongs with the money-flow tracking — because "yield or
shelter" is literally the question *where is money going*.

### 2 · The four economic regimes

Growth × inflation, the canonical two-by-two:

| | High inflation | Low inflation |
|---|---|---|
| **Strong economy** | strong economy · high inflation | strong economy · low inflation |
| **Weak economy** | weak economy · high inflation | weak economy · low inflation |

---

## ⏱️ And the reason they never merge into one number

> **The quadrant is slow (months). The risk appetite is fast (days). Volatility is
> instantaneous (minutes).**

They are kept as **separate fields**, never fused.

> [!TIP]
> **Because the disagreement is the information**
>
> When the slow measure and the fast measure disagree, that is not an error to
> reconcile — **it is one of the most informative states the record can hold.**
> Merge them into one score and that information vanishes silently, with nothing in
> the logs to show it ever existed.

---

## Where the values come from — and where they do not

| What | Source |
|---|---|
| the two macro definitions | two published frameworks, used **in parallel**, credited as third-party claims |
| the risk axis | published indices, without a threshold of our own invention |
| volatility | our own candles |
| **bitcoin's behaviour by quadrant** | ⚫ **no established knowledge** — bitcoin has lived through roughly one macro cycle |

That last row is the honest one. Asset-rotation behaviour by regime exists in the
literature for traditional assets. For bitcoin it does not, and one cycle proves
nothing. So it is recorded as a hypothesis with a mechanism for accumulating
evidence — every outcome records its regime, and after a hundred outcomes *"do results
differ by quadrant"* becomes an ordinary query.

---

## 🚧 A borderline month is a value, not a gap

When the two macro definitions disagree, the system does not pick a winner and does
not fall back to a default. It sets `quadrant_agreed = False` and **asserts no
regime**.

That state has its own row in the decision table, with its own outcome. Uncertainty
is represented, not smoothed over.

This is the same instinct as an earlier lesson the project paid for:

> **If a view has only two colours, "I don't know" will get painted the good one.**

---

## ⚠️ The trap, written down in advance

> [!CAUTION]
> A regime is **a narrative over numbers** — and narrative is exactly what killed an
> earlier pattern: choosing an explanation after the fact, from among five things that
> happened to occur.
>
> Therefore, when its turn comes, the regime is recorded **as a dated field, before it
> is known what happened next.** It is never assigned retroactively to a past day.
>
> Otherwise the archive begins explaining its own past to itself, and every check
> against it becomes meaningless.

That single paragraph is, in miniature, the whole reason this project writes things
down before it needs them.

---

## ⚠️ What is not being claimed

- No regime layer exists as code.
- Not one threshold is calibrated.
- Volatility does not yet have a definition — which number measures it, over which
  window, is an open question.
- Bitcoin's behaviour by quadrant is a hypothesis.

---

## 🔗 Related

[Smart money track](Smart%20money%20track.md) · [The daily file](The%20daily%20file.md) · [Principles](../01%20%E2%80%94%20THE%20IDEA/Principles.md)
