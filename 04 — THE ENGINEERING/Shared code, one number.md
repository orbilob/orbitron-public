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

> **You prove one number and you trade a different one, and the difference is
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
strategy/            imports it · the glue to freqtrade (~50 lines)
collector/           does NOT import it — it fetches and writes, it computes nothing
```

The last line is the one that matters for security: the collector runs on the most
exposed machine, and it does not even *have* the analytical code to leak.

---

## The one thing the shared package must never import

> **The shared package imports nothing from freqtrade.**

This is a legal boundary (freqtrade is GPL-3.0) and an architectural one at the same
time: the head does not know which hand executes it.

The two boundaries reinforcing each other is not a coincidence — a clean licensing
story and a clean dependency story usually turn out to be the same story.

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

## The related principle: one definition per quantity

Every quantity the project stands on has a **written definition** — what it
measures, which rows it is computed from, when it is invalid. Not "an ATR", but
*this* ATR, with a version.

The failure mode this prevents is subtle and common: two modules both compute
"volatility", both are correct by their own definition, and a comparison between
them is meaningless in a way that no error message will ever reveal.

---

## 🔗 Related

[Repositories](Repositories.md) · [Contracts and formats](Contracts%20and%20formats.md) · [The detachable tool](The%20detachable%20tool.md) · [The v2 backtest engine](The%20v2%20backtest%20engine.md)
