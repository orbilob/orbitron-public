← [START HERE](../START%20HERE.md)

# 🧩 Shared code, one number

> [!TIP]
> **The rule**
>
> **The same input yields the same number, no matter who calls it.**

Indicators, scoring, passports, regimes and signal generation live in **one shared
package** that everything else imports. Nothing is transcribed by hand from one
repository into another.

---

## The rule this replaced — and why it was wrong

The project's first architecture forbade imports between repositories on purpose:
the lab would *prove* the logic, and the production core would *rewrite it from
scratch*.

The reasoning was not stupid. A rewrite is a second pair of eyes: if you can
reimplement it from the description, you understood it.

But the cost turned out to be larger than the benefit:

> **You prove one number and you act on a different one, and the difference is
> invisible until it costs money.**

The replacement rule is testable. "We rewrote it carefully" is not.

---

## What lives where

```
shared package/      ← imported by everything, knows about nobody
  ta/                indicators — one ATR, one definition
  fa/  sentiment/     fundamentals, sentiment
  regimes/           market regimes
  smart_money/
  scoring/           weights and thresholds
  passports/         the pattern passport
  press/             signal from passport + detect()

lab/                 imports it · measures with the v2 engine
tools/               import it · never the other way round
collector/           does NOT import it — it fetches and writes, it computes nothing
```

The last line is the one that matters for security: the collector runs on the most
exposed machine, and it does not even *have* the analytical code to leak.

---

## The direction of dependency never reverses

> **The shared package imports nothing from anything above it.**

It knows about indicators and definitions; it does not know who is calling it or
why. That is what makes the rule testable at all — a package that reaches upward
into its callers cannot promise the same number from every direction.

---

## The test that enforces it

The rule is phrased the way it is so that it can be a test rather than a review
comment:

```
given the same candles,
the indicator called from the lab and the indicator called from the live chain
must return the same number.
```

If they don't, one of them is wrong and you find out in CI rather than in a
post-mortem.

---

## One engine for the data

The rule above has a precondition that is easy to miss: **both callers must compute
on the same engine.** For a while the lab ran on polars and everything else on
pandas, and both sides claimed to do the same arithmetic. That claim could not be
tested — a comparison across two libraries checks two implementations, not one
piece of logic in one place. Decided on 15.09.2026: **pandas everywhere.**

Speed was the argument for polars, so it was measured rather than assumed. One
year of one-minute candles, 525,600 rows: the ATR takes 92 ms in pandas and 17 ms
in polars. Five times faster, and 75 ms that nobody waits for.

Two differences had to be settled by hand, and they will come back with any
similar switch:

| Difference | What happens if it is missed |
|---|---|
| **Ties** | polars `sort_by(...).last()` keeps the *last* of equal values, pandas `idxmax` the *first*. A drop and a rebound of equal size flip an event from bearish to bullish |
| **A column that can be empty** | pandas `int64` cannot hold a missing value; it either raises or silently becomes a float. The nullable `Int64` is required |

The port was checked by differential probes: the old version, taken from history,
against the new one on the same input. All 24 columns of the first pattern agree,
the largest gap being `2.5e-14` — floating-point noise. And the suite passes with
polars **deliberately blocked** from import.

> [!NOTE]
> Two of the probes could not fail at first. A threshold broken on purpose passed
> because no row sat exactly on it; a broken `idxmax` passed because the cluster
> had a single maximum. *A test that cannot fail is worth nothing* holds for probes
> too.

---

## The related principle: one definition per quantity

Every quantity the project stands on has a **written definition** — what it
measures, which rows it is computed from, when it is invalid. Not "an ATR", but
*this* ATR, with a version.

The failure mode this prevents is subtle and common: two modules both compute
"volatility", both are correct by their own definition, and a comparison between
them is meaningless in a way that no error message will ever reveal.

---

## 🔗 Related

[Repositories](Repositories.md) · [Contracts and formats](Contracts%20and%20formats.md) · [The v2 validation engine](The%20v2%20validation%20engine.md)
