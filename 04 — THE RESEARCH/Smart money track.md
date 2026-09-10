← [[START HERE]]

# 🐋 Smart money track

> The question is not *"is the price going up"*. It is **"where does money go when it
> leaves somewhere else"**.

---

## The four destinations

When money exits one place, it has to arrive somewhere. Four candidates are tracked:

| Destination | What is measured |
|---|---|
| 🥇 **Gold** | the spot price — not an ETF proxy |
| 🏛️ **Government bonds** | the yield curve across maturities, plus a measure of bond-market stress |
| ₿ **Crypto** | the whole collector — candles, volume, open interest, funding |
| 📈 **Equities & ETFs** | fund flows into bitcoin products, and equity-market level as part of the macro picture |

---

## One field, one quantity

A small decision with a large shape, and a good example of how format discipline
prevents confusion later.

"ETF" turned out to mean two different things:

1. **the stock market in general** — an indicator of whether money is in equities at all;
2. **bitcoin ETF flows** — which is really the crypto destination, seen from outside.

The answer was not to choose. It was:

> **Both — at two different addresses.** The bitcoin fund flow is a **flow** and lives
> in smart money tracking. An equity index is a **level** and lives in the regime.
>
> **One field does not carry two quantities.**

---

## ⭐ How it enters a trading decision — the interesting part

This is where smart money differs from every other input in the system, and it is
the project's favourite piece of design.

> **Smart money does not raise confidence. It tightens the stop.**

When price is in a zone that institutional players defend in our direction, that does
not make the signal *more true*. It makes the stop **cheaper** — a stop just beyond
the zone risks less for the same trade.

Why this is better than "add some points":

| Raising confidence | Tightening the stop |
|---|---|
| → larger position size | → the same risk over a shorter distance |
| → **more risk** | → **a smaller loss when we are wrong** |

And the arithmetic agrees: leverage is a *result* of risk and stop distance. Tighten
the stop at constant risk and leverage rises — so the lever is not free, and the
risk-management ceiling still applies above it.

That is why, in the decision order, smart money runs **last and outside the
confidence calculation**. It is a parameter of the trade, not a vote on it.

---

## Where it surfaces

In a section of the daily file titled `daily info & smart money track` — today a
human-written paragraph about the day, tomorrow the same place enriched with the
regime and the flows.

The section title was chosen in advance precisely so it would never need to change
between the private archive and the public view. A heading that differs between two
places is two names for one thing.

---

## ⚠️ What is not being claimed

- The lever does not exist as code.
- **"Smart money zone" has no written definition yet** — what a zone is, which rows
  it is computed from, and when it is invalid.
- The tracking module exists in name; the mechanism does not.

---

## 🔗 Related

[[Market regimes]] · [[The daily file]] · [[STRATEGY ENGINE]]
