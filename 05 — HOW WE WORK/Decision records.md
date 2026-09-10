← [[START HERE]]

# ⚖️ Decision records

> Every decision that is expensive to reverse gets **its own file**.

Not a line in a changelog. Not a paragraph in a design document. A file, with a
date, a set of criteria, the candidates, and a table of arguments where **every cell
carries a label**.

---

## The shape of one

```
# D12 — The detachable tool

✅ DECIDED · 2026-09-10
   [the decision, in one sentence]

## The decision, in one word
## What it means in practice        ← a table of conditions and how each is met
## Where it applies today
## Why — the arguments              ← each labelled ✅ / 🟡 / ⚫
## What would overturn this
## 🔗 Related
```

The last two sections are the ones most projects skip, and they are the ones that
make the format worth the trouble.

---

## "Decided on DATE, because…" — never "not open for discussion"

A recorded decision is **the current best answer, with a date and a reason**. It is
not a constitution.

> **The reasoning is preserved because it states what would have to be overturned.**

That is the whole trick. A decision recorded as a conclusion can only be defended or
abandoned. A decision recorded with its reasoning can be **re-examined against new
evidence** — you check whether the reason still holds.

And it makes a rule possible that would otherwise be uncomfortable:

> Everything is subject to change according to the operator's judgement. The agent
> does not defend yesterday's decision against today's wish — it recalls the reasoning
> and then executes.

---

## "What would overturn this" — written at decision time

Every significant decision ends with a section naming the evidence that would reverse
it. Written **while deciding**, not afterwards.

Two examples from the vault:

> **On not building a vector search over the documentation:**
> *"What would overturn this: a vault of several thousand documents, or material in a
> form that plain-text search cannot reach — scanned PDFs, images."*

> **On keeping the documentation's prose in the author's native language while all
> code is English:**
> *"What would overturn this: a decision to move the whole vault to English, or the
> repositories ceasing to cite the vault at all."*

The value is that it turns a future argument into a **check**. Instead of two people
disagreeing about a decision from eight months ago, someone looks at the named
condition and asks whether it has happened.

---

## Why this beats a changelog

A changelog tells you **what changed**. A decision record tells you **what was true
when someone chose, and what they were afraid of**.

Six months later, the first is trivia and the second is the only thing that lets you
decide whether the choice still applies.

---

## The cost, stated fairly

It is slower. Writing a decision record for something you already "just know" feels
like ceremony, and roughly one in four turns out never to be read again.

The other three pay for all of them the first time somebody — human or AI — starts
re-opening a settled question. That is the trade, and it is only worth it for
decisions that are **expensive to reverse**. Everything else gets a commit message.

---

## 🔗 Related

[[Evidence labels]] · [[Working with an AI agent]] · [[Guards and the generated map]]
