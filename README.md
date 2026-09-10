<div align="center">

<img src="assets/logo.png" alt="ORBITRON" width="380">

# ORBITRON — public vault

**Understanding market mechanics. Trading is the instrument, not the goal.**

[![Vault guard](https://github.com/orbilob/orbitron-public/actions/workflows/vault.yml/badge.svg)](https://github.com/orbilob/orbitron-public/actions/workflows/vault.yml)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-2ecc71?style=flat-square)](LICENSE)
[![Research project](https://img.shields.io/badge/research-not%20a%20trading%20bot-f39c12?style=flat-square)](01%20%E2%80%94%20THE%20IDEA/Why%20this%20exists.md)
[![Obsidian vault](https://img.shields.io/badge/Obsidian-vault-7c3aed?style=flat-square&logo=obsidian&logoColor=white)](https://obsidian.md)

**The stack**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)
[![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)](https://numpy.org)
[![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=flat-square&logo=scipy&logoColor=white)](https://scipy.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![freqtrade](https://img.shields.io/badge/freqtrade-detachable-64748b?style=flat-square)](04%20%E2%80%94%20THE%20ENGINEERING/The%20detachable%20tool.md)

**Written with**

[![Claude Code](https://img.shields.io/badge/built%20with-Claude%20Code-D97757?style=flat-square)](https://claude.com/claude-code)
[![Under written rules](https://img.shields.io/badge/under-written%20rules-2ecc71?style=flat-square)](05%20%E2%80%94%20HOW%20WE%20WORK/Working%20with%20an%20AI%20agent.md)

</div>

---

### **This is not a trading bot.**

It is an attempt to understand **how markets actually work** — why a trend moves in
the direction it does, and what is happening behind the scenes.

Markets never stop changing. The thing that worked last quarter stops working, and
usually nobody can say exactly when it stopped or why. Explanations arrive
afterwards, confidently, and cannot be checked.

So this project does two things instead:

> **It keeps a permanent, honest record of what markets did and what the world looked
> like while they did it — and it builds instruments for asking that record hard
> questions.**

Trading is one of those instruments. Paper trading turns a claim about mechanism into
something that can come back **negative** — measured against chance, after costs,
corrected for testing many things at once. A pattern that earns money is *evidence
that some mechanism was understood correctly*. That is the only reason profit
interests this project at all.

**→ [Why this exists](01%20%E2%80%94%20THE%20IDEA/Why%20this%20exists.md)** — the full
argument, in five minutes.

---

## 🏆 The part that matters most

> **Raw candles can be re-downloaded from the exchange at any time.
> The explanation of a day cannot.**

Every day is recorded as a single image — the macro backdrop, the flows, the mood,
what was known and what wasn't — written once, in the moment, and kept **forever**.
A daily file weighs a few kilobytes; a century of them weighs less than one day of
raw candles.

It makes a question possible that cannot be asked today:

> *"Find me the days whose macro image resembles today's — how did this mechanism
> behave then?"*

Only someone who started keeping the record years earlier can ask it.
→ [The golden archive](02%20%E2%80%94%20THE%20RESEARCH/The%20golden%20archive.md)

---

## 🚪 Where to start

This is an **[Obsidian](https://obsidian.md) vault**. Clone it and open the folder as
a vault, or just read it here on GitHub — the folder names are the table of contents
and every link works in both.

| You are | Start here | Time |
|---|---|---|
| 🧑 Curious, non-technical | [Why this exists](01%20%E2%80%94%20THE%20IDEA/Why%20this%20exists.md) | 5 min |
| 🔬 Interested in method | **02 — THE RESEARCH** and [The v2 backtest engine](04%20%E2%80%94%20THE%20ENGINEERING/The%20v2%20backtest%20engine.md) | 15 min |
| 🧑‍💻 A developer | **04 — THE ENGINEERING** and **05 — HOW WE WORK** | 20 min |

Full map: **[START HERE](START%20HERE.md)**

```
01 — THE IDEA          why this exists · what it is and is not · principles
02 — THE RESEARCH      the permanent archive · regimes · smart money · the daily file
03 — THE SYSTEM        how observation becomes a testable claim
04 — THE ENGINEERING   contracts, statistics, and the boundaries that keep it honest
05 — HOW WE WORK       ⭐ the discipline: decisions, evidence labels, guards
```

---

## ⚠️ Disclaimer

**ORBITRON is personal research. Nothing here is financial advice.**

- It does not sell signals, subscriptions, copy-trading or a course.
- It does not manage anyone else's money, and never will.
- **No claim of profitability is made anywhere in this vault.** The measure of
  success at this stage is honesty, not return.
- Any numbers you find are illustrations of method, not a track record.
- Large parts of what is described here are **designed, not built** — and where that
  is the case, the documents say so in a section titled *"what is not being claimed"*.

If you came looking for a system that makes money, this is the wrong repository.
If you came looking for how someone tries to understand a system that refuses to hold
still — welcome.

---

## 🔒 What is deliberately not here

Infrastructure details, network layout, hostnames, credentials, calibrated
thresholds, scoring weights, and the pattern code itself.

**What is shown is how the project thinks. What is withheld is what it trades on.**

---

## 📄 License & authorship

Documentation by **Joro the Best**, written together with an AI agent working under
the project's own written rules — see
[Working with an AI agent](05%20%E2%80%94%20HOW%20WE%20WORK/Working%20with%20an%20AI%20agent.md).

Licensed under [CC BY-NC 4.0](LICENSE) — read it, share it, quote it with credit;
don't sell it.
