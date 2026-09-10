← [[START HERE]]

# 🏷️ Evidence labels

> [!success] The rule
> A fundamental decision stands on **arguments, not brochures**.

Every claim in a decision table carries a label. Three of them, and the third is the
one that makes the system work.

| Label | Means |
|---|---|
| ✅ **verified** | seen in code, in the primary source's own documentation, or measured by us |
| 🟡 **claimed** | somebody says so — an article, another AI, a forum. Not verified |
| ⚫ **unknown** | we don't know, and we admit it |

> **A decision whose arguments are all 🟡 is not a decision — it is a repetition of
> somebody else's opinion.**

---

## Why ⚫ is the valuable one

✅ and 🟡 are ordinary source hygiene; most careful projects have some version of
them.

The third label is the one that changes behaviour, because it makes **"I don't know"
a first-class value that survives into the document.** Without it, unknowns get
quietly rounded to whichever neighbouring value is convenient — and nothing in the
text ever reveals that a gap was there.

This mirrors a lesson the project paid for in a completely different area:

> A reader returned "no threshold defined", the view treated that as "on time", and
> painted a green dot on a row that was six days stale.
>
> **If a view has only two colours, "I don't know" will get painted the good one.**

Since then, every new display element goes through one question before it is drawn:
**"what does this show when it doesn't know?"**

---

## ⚠️ "What is not being claimed" — a required section

The most useful convention in the whole vault, and the cheapest to adopt.

Design documents in this project end with a section listing, explicitly, what does
**not** exist yet:

> **What is not being claimed**
> - None of this stage exists as code. ⚫
> - There is no fixed JSON schema. ⚫
> - Not one threshold or weight is calibrated.
> - The field-length limit has not been verified. ⚫
> - The structure came from third-party material and was assessed as data, not
>   accepted as truth.

Why it matters so much here: **a document written in the present tense reads as
description of something that exists.** Architecture is conventionally written that
way, and the convention quietly lies whenever the thing is still a plan.

The session handover file carries the same section, for the same reason — it protects
the next session from building on an imaginary foundation.

---

## The related rule for measurement

> **A metric without a baseline is advertising.**

Every number answers "compared to what". An answer of "compared to nothing" voids it.

And its companion:

> **The success criterion is derived from the mechanism, not accepted ready-made.**

A real example: a recorded test was *"a spike in bond-market stress → confirmation"*.
It sounded plausible and was looking for **the opposite sign**. If the mechanism is
`Treasury action → yields → dollar → crypto`, then that stress index was never the
right test. Plausible and wrong is the expensive combination.

---

## 🔗 Related

[[Decision records]] · [[Principles]] · [[The v2 backtest engine]] · [[Working with an AI agent]]
