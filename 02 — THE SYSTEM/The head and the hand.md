← [[START HERE]]

# 🧠 The head and the hand

> [!success] The load-bearing decision
> **The hand is [freqtrade](https://www.freqtrade.io). The head is ours.**

---

## The split

| Who | What it does |
|---|---|
| 🧠 **ORBITRON** | technical analysis · fundamentals · sentiment · smart money · market regimes · scoring · passports · the press · the trade calculation · the journal · the database |
| 🖐️ **freqtrade** | holds the exchange connection · sends the order · keeps the stop · watches the position · backtests · runs paper trading |

Between them sits **thin glue** — a strategy file that decides nothing and only
asks the core a question and passes the answer along. In the current
implementation that glue is about fifty lines and contains **not one conditional
statement**.

That number is not trivia. It is the measurement that proves the boundary is real:
logic cannot leak into a file that has no branches in it.

---

## Why borrow the hand at all

Because exchange plumbing is a solved problem, and solving it again would be
expensive in exactly the way that teaches you nothing:

- reconnects, rate limits, partial fills, order-state edge cases
- stop orders that survive a process restart
- a paper-trading mode that behaves like the live one
- a backtest runner and a working UI

None of that is market mechanics. All of it is weeks of work and a long tail of
bugs that only appear with real money on the line.

## And why the head is never borrowed

Because the head **is** the project. Understanding what moves prices is the point;
the order-sending is the test harness around it.

---

## Two boundaries that are never crossed

### ⚖️ The legal one

freqtrade is licensed under **GPL-3.0**. Therefore:

- it is **not forked**
- **not one of its files is modified**
- it is extended only through the extension points it provides
- **our core imports nothing from it**

The last point is the important one. It means the core could be shown publicly
without a single question about its provenance.

### 🔌 The architectural one

The same boundary, arrived at from a completely different direction:

> **Remove the tool in your head. If the project stops working, it was not a tool —
> it was a foundation, and the rule is broken.**

This is a general rule about all third-party software, not a special arrangement for
freqtrade. It has its own page: [[The detachable tool]].

---

## What this decision made unnecessary

Worth recording, because it is the clearest evidence that the split was the right
one.

An earlier architecture had the home server *commanding* a remote machine to place
trades. That required a whole security apparatus: an execution gateway, HMAC
signatures, a nonce counter, clock synchronisation between machines, self-locking
on failure.

All of it existed to solve one problem: **how does a server safely instruct another
machine to trade?**

When freqtrade moved to run where the decision is made, the question disappeared, and
the entire apparatus went with it. There are no commands to sign, because there are
no commands.

> The cheapest security design is the one you delete.

---

## 🔗 Related

[[The chain]] · [[The detachable tool]] · [[STRATEGY ENGINE]] · [[The three machines]]
