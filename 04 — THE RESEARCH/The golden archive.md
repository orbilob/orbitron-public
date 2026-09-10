← [[START HERE]]

# 🏆 The golden archive

> [!success] The rule
> **The daily files are kept forever.** No rotation. No deletion of old files.
> One day = one file, permanently.

---

## The sentence the whole idea rests on

> **Raw candles can be re-downloaded from the exchange at any time.
> The explanation of a day cannot.**

The explanation is written once, in the moment, and can never be reconstructed after
the fact. Not because the data is gone — because *the way the day looked while it was
happening* is gone. Hindsight rewrites it silently and convincingly.

That asymmetry is the entire argument. Everything else is a consequence.

---

## The cost, honestly

A daily file is a few kilobytes. **A century of text weighs less than one day of raw
candles.**

There is no storage argument against this, which is precisely why it is worth being
strict about: the only way to lose the archive is by deciding to.

---

## What it grows into

```
   [ daily archive ]      ← this part is being built now
         │
         │  grows by adding fields, not by being rebuilt
         ▼
   [ permanent archive ]  ← the full daily image:
                             technical · fundamental / geopolitical
                             macro · on-chain / DeFi · sentiment
         │
         ▼
   [ questions we cannot ask today ]
     "find me the days whose macro image resembles today's —
      how did the pattern behave then?"
```

The key idea is the one that runs through the whole project:

> **Context turns a number into an event.** The same technical state means different
> things under different liquidity, a different macro backdrop, a different mood.

So each passing day is recorded as a **single image** — not only what the price did,
but what the world around it looked like.

> [!danger] None of the far end goes into code now
> This describes a **direction, not a task**. The heavy part — a different database,
> vector representations, a language-model pipeline — arrives the day the project has
> grown enough to require it. Until then a simple embedded database is enough, and the
> daily file grows by adding fields.

That restraint is deliberate and is itself a design decision. The archive is built so
that the expensive version becomes possible later **without rewriting anything**.

---

## The rule that makes the archive trustworthy

> **A value enters a given day only if it was publicly known by the end of that day.**
> Missing values are carried forward, never backward.

Without that rule an archive slowly fills with information from the future, and every
backtest run against it becomes a lie that nothing detects.

It pairs with the regime rule from [[Market regimes]]: a regime is recorded as a
**dated field, before it is known what happened next** — never assigned retroactively.

---

## 💾 And the one open question

A backup strategy — a physical drive plus a cloud copy — is recorded as an
**intention, not a plan**. The details (which cloud, what frequency, what encryption)
are a separate decision.

It is worth doing for this archive specifically because it is **small and
irreplaceable** — the exact opposite of the candle database, which is enormous and
replaceable.

---

## 🔗 Related

[[The daily file]] · [[Market regimes]] · [[Contracts and formats]] · [[What ORBITRON is]]
