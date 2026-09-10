← [START HERE](../START%20HERE.md)

# 📦 Repositories — three, not more

| Repository | Contains | Runs on | Why separate |
|---|---|---|---|
| 📡 **COLLECTOR** | everything that fetches from outside and computes nothing | ☁️ the cloud machine | **Security**: that machine physically cannot see the analysis code, even by mistake |
| ⚙️ **CORE** | technical + fundamental analysis, the engine, the trade calculation, the dashboard | 🏠 the home server | They evolve together, with frequent cross-cutting changes |
| 🧪 **LAB** | research, backtesting, history | 💻 the command centre | A completely different lifecycle |

Plus this vault and the private working vault, which carry no code and do not count.

---

## The reasoning behind each split

### Why the collector is alone

Not modularity — **blast radius**. The collector is the only component with an
inbound relationship to the open internet, and it runs on the machine designated as
*acceptable to lose*. Keeping the analytical code out of that repository means a full
compromise of that machine leaks nothing worth having.

### Why the core is one repository and not four

The four logical areas inside it (technical analysis, fundamentals, the trade
calculation, the dashboard) change together constantly. Splitting them would buy
imaginary independence and pay for it in cross-repository version dances.

> **The repository solves coordination** — one git history, atomic commits.
> **The processes solve stability** — each area runs as its own OS process,
> communicating only through the shared database.

That is the actual separation of concerns; the folder layout is not.

### Why the lab is alone

A different lifecycle entirely. Research code is allowed to be exploratory, messy
and thrown away. Production code is not. Mixing the two means one of those standards
wins, and it is never the strict one.

Critically: **the lab does not participate in the live chain and does not dictate
formats.** Its product is patterns that meet a single standard.

---

## What crosses between them

Only two things, both of them contracts rather than calls:

- **The shared package** — one input, one number, imported by everyone who computes.
  See [Shared code, one number](Shared%20code%2C%20one%20number.md).
- **The data schema** — a versioned contract for the tables that two repositories on
  two machines both read.

And the compatibility requirement runs **both ways**: every row the collector writes
must be usable in the lab without conflict, and every pattern leaving the lab must be
compatible with the rest. No translation anywhere along the path.

---

## 🔗 Related

[The three machines](../03%20%E2%80%94%20THE%20SYSTEM/The%20three%20machines.md) · [Shared code, one number](Shared%20code%2C%20one%20number.md) · [Contracts and formats](Contracts%20and%20formats.md) · [The chain](../03%20%E2%80%94%20THE%20SYSTEM/The%20chain.md)
