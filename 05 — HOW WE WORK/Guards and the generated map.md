← [START HERE](../START%20HERE.md)

# 🛡️ Guards and the generated map

Documentation rots. This is the mechanical part of not letting it.

Two scripts run **before every commit**. One checks the vault for self-contradiction;
the other regenerates the index so that it cannot go stale.

---

## Why a guard was needed at all

The honest origin story: at one point the vault had **19 broken links**, stale paths
in 8 files, and the complete plan of a closed phase still sitting in the "current
work" document — and nobody could see it.

> A document that points into the void sends the agent to the wrong place **with
> confidence**. A ticked-off item in a list of "active tasks only" is history that
> reads as work.

Neither is caught by reading. Both are caught by a script in under a second.

---

## What the checker verifies

| # | Check | Why |
|---|---|---|
| 1 | **Broken links** — to a file that doesn't exist, or a heading that doesn't exist | the wrong-place-with-confidence problem |
| 2 | **Stale paths** — folders that no longer exist in this vault | a line containing one is a layer from a previous structure |
| 3 | **Ticked-off items** in the "current work" and "backlog" files | done work is removed, not decorated |
| 4 | **The index is older than the last change to the vault** | a reminder to regenerate |
| 5 | **Rule codes that don't exist** | catches a citation to a rule that was renamed or removed |
| 6 | **Rules cited by number instead of by code** | the seven-wrong-references problem |
| 7 | **Twin phrases** — a statement that must match in two places | the anti-drift check |

Exit code 0 = clean. Exit code 1 = there is something to fix, and every line says
where.

> [!TIP]
> **The guard is the enforcement of "one statement, one place"**
>
> A red check means something is recorded in two places or points into nothing. It
> gets fixed before the commit, not worked around.

Check 7 deliberately looks **outside** the vault too — into the code repositories,
when they are present. A missing repository is skipped silently, because working with
one repository attached is the normal mode, not an error.

---

## 🗺️ The map is generated, never written

The vault's index — *which file is about what · where a concept is defined · what was
decided and when* — is **machine-generated** and regenerated in the same commit as
any change.

This is the point:

> **A hand-maintained index is a second source of truth. A generated one cannot
> disagree with the vault, because it is derived from it.**

It is also the first thing read at the start of every session, which makes its
freshness load-bearing rather than cosmetic.

---

## 🔎 And why there is no vector search

A decision worth including because the answer went against the fashionable choice:

> **235 files with descriptive names and a generated index are not a semantic search
> problem.**

Vector search returns "the closest thing by meaning". This project needs
**exhaustiveness** — the rule "one statement, one place" requires finding *every*
occurrence, not the nearest one.

And the project's vocabulary is a trap for embeddings: one term names two different
things (a repository and the machine it runs on), one string is a filename rather
than a concept, one section heading is deliberately in a different language from the
text around it.

> **Plain-text search distinguishes them precisely because it does not understand
> them.**

*What would overturn this: a vault of several thousand documents, or material that
plain-text search cannot reach — scanned PDFs, images.*

---

## The single-source-of-truth rule for status

One more mechanism worth stealing:

> **Exactly one document says whether something is finished.**

Reference documents describe **how** a thing works. They never say whether it is
built. A single live status board says how far each component has got.

> A disagreement between two documents about what is done becomes **physically
> impossible**, because only one of them is allowed to have an opinion.

---

## 🔗 Related

[Decision records](Decision%20records.md) · [Evidence labels](Evidence%20labels.md) · [Working with an AI agent](Working%20with%20an%20AI%20agent.md) · [Contracts and formats](../04%20%E2%80%94%20THE%20ENGINEERING/Contracts%20and%20formats.md)
