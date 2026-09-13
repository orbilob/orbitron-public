← [START HERE](../START%20HERE.md)

# 🍅 The tomato press

> [!NOTE]
> **The operator's analogy**
>
> *"We buy ten different tomatoes from the market. We put them in the press. One
> squeeze — and out comes tomato purée, regardless of whether the tomato was big or
> small."*

This is the founding analogy of the whole data architecture, and it is worth more
than the diagram it replaced.

| In the analogy | In the system |
|---|---|
| 🍅 the tomatoes | the patterns — all different, each with its own character |
| 🔧 the press | the slot — one machine, one output |
| 🥫 the purée | the record in the archive — **one format, always** |
| 🔴 a ripe red tomato | a proven pattern (`validated`) |
| 🟢 a sour green one | a pattern still in development (`observation`) |

**The green tomato goes into the same press.** Its purée is more sour, but it is the
same product, in the same jar, **with a label**.

That is exactly why the status field in a pattern's passport is mandatory: a jar
without a label is a mystery a year later.

---

## Two things called "slot"

The word is used in two senses, and separating them removes a recurring confusion:

**The slot as a machine** — the code that takes a pattern and produces a record. The
press. There is one, it is fixed, and it is not modified when a new pattern arrives.

**Slots as positions** — how many patterns run at once. Three openings in the press,
currently all three occupied. Three is not a technical limit; it is a decision about
how many patterns to watch simultaneously. A fourth row in the pattern registry
works without touching the machine.

```
         [ ORPROBE ]
              │
    ┌─────────┴──────────┐
    │  THE PRESS (slot)  │  ← one machine
    ├────────┬─────┬─────┤
    │ pos. 1 │ 2   │ 3   │  ← how many at once
    └────────┴─────┴─────┘
              │
         one purée
              ▼
      [ signals table ]
```

---

## Why formats come before logic

ORBITRON is a research project. Patterns will be born, mutate and die — that is
their normal behaviour, not a problem.

But if every pattern has its own record format, then six months later you cannot
compare pattern A001 with pattern A007. The data is incomparable and the entire
accumulated history is worthless.

> **So: the frame is frozen now, while it is cheap. The patterns line up inside it
> afterwards.**

This principle repeats across the project — the decision passport, the daily file,
the database schema. It has its own page: [Contracts and formats](../04%20%E2%80%94%20THE%20ENGINEERING/Contracts%20and%20formats.md).

---

## The consequence for scale

The press never asks what the time step of its input is. Neither does its research
counterpart. Daily candles go through the same contract as one-minute candles.

That single property is why the project can claim to be scale-neutral without
having built anything special for it.

---

## 🔗 Related

[The chain](The%20chain.md) · [Contracts and formats](../04%20%E2%80%94%20THE%20ENGINEERING/Contracts%20and%20formats.md) · [The v2 validation engine](../04%20%E2%80%94%20THE%20ENGINEERING/The%20v2%20validation%20engine.md) · [The eternal archive](../02%20%E2%80%94%20THE%20RESEARCH/The%20eternal%20archive.md)
