← [START HERE](../START%20HERE.md)

# 🧱 Contracts and formats

> [!NOTE]
> **The rule**
>
> **Formats are frozen before the logic that fills them.**

Three contracts are fixed ahead of any pattern logic: the **pattern passport**, the
**signal record**, and the **daily archive**. They are the fixed core; the patterns
are the flowing sands.

---

## Why this order

Patterns will be born, mutate and die. That is their normal behaviour.

But if every pattern writes its own record format, then six months later A001 cannot
be compared to A007. The data is incomparable and the accumulated history is
worthless.

> The frame is frozen while it is cheap. The patterns line up inside it afterwards.

And there is a second reason, specific to the head/hand boundary:

> **A boundary expressed as a format is also the test for detachability.** A function
> call can only be verified by running it. A format can be compared against
> yesterday's without starting anything.

---

## 📋 The passport convention

Every module declares its inputs, outputs, version and compatibility. For a pattern
that means: the hypothesis, the direction, the family, the lookback, and — mandatory —
the **status**.

| Status | Meaning |
|---|---|
| `observation` | in development. Still ripening |
| `validated` | passed the v2 engine with significant edge |

The status is mandatory for the reason the tomato analogy gives:
**a jar without a label is a mystery a year later.** See [The tomato press](../03%20%E2%80%94%20THE%20SYSTEM/The%20tomato%20press.md).

---

## 🔁 Compatibility is a two-way contract

Not "we try to make it fit". An actual bidirectional requirement between the three
repositories:

> **Every row written by the collector** must be usable in the research lab **without
> conflict**, and embeddable into a method.
>
> **Every pattern that leaves the lab** must be **fully compatible** with the other
> repositories.

Three consequences for daily work:

1. **There is no translation anywhere along the path.** A field renamed between two
   repositories is a defect, not a convenience.
2. **A format change is a change in all three places, in one commit.**
3. **The format has a version and must survive time** — a daily file from six months
   ago is read by today's reader.

---

## 🕰️ Versioning, and what it actually buys

`schema_version` is the first field of the decision passport. Not the third, not
optional.

Without it, the sentence *"a file from six months ago is read by today's reader"* is
a wish. With it, it is a requirement that can be tested — and a reader can decide
what to do about an old version instead of silently misreading it.

The same logic drove a real decision about pattern versions: an entry recorded under
version 1.1 with one set of parameters is not the same event as one recorded under
version 2 with different parameters. Rewriting the old records to match the new
version would make the archive lie about its own past.

---

## 🗄️ And the same discipline in the database

The database schema is a **versioned contract**, because tables like `candles` and
`funding_rate` are read by two repositories on two machines. A schema that lives in
only one of them drifts.

One deliberate decision worth mentioning: **table, column and index names are in
English**, including inside a project whose thinking is done in another language.
The reasoning is the same as the rest of this page — the data outlives the session
that created it, and a name is a contract with the future reader.

---

## What a good format decision looks like

An example from the project, kept because it is a small decision with a big shape:

> A field must carry **one quantity**. When it turned out that "ETF" meant two
> different things — a *flow* (money entering bitcoin funds) and a *level* (whether
> money is in equities at all) — the answer was not to pick one. It was two metrics
> at two addresses.
>
> **One field does not carry two quantities.**

---

## 🔗 Related

[The tomato press](../03%20%E2%80%94%20THE%20SYSTEM/The%20tomato%20press.md) · [The eternal archive](../02%20%E2%80%94%20THE%20RESEARCH/The%20eternal%20archive.md)
