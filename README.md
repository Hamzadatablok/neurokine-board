# 🧠 NeuroKine Board — AI Multidisciplinary Medical Committee

Instead of a single AI answer, **NeuroKine Board** convenes a *virtual committee*
of four specialized AutoGen agents who **discuss** a patient/athlete case until
they agree on a safe, unified return-to-play / rehabilitation protocol.

> You don't get a chatbot. You get a full AI-powered medical board consultation.

---

## 🧩 The Committee

| Agent | Role |
|-------|------|
| 🦵 **Kinesiology Expert** | Analyzes movement, biomechanics & injury — calls the scientific tools |
| 🧠 **Sports Psychologist** | Assesses fear of re-injury, motivation and stress |
| 📊 **Data & Biomechanics Analyst** | Interprets numeric data (VO2 max, HR, joint angles, ACWR) |
| 🛡️ **Safety & Ethics Auditor** | Reviews the plan for harm; signs off with `APPROVED` |

You act as the **Admin**: you present a case, the committee discusses it in a
dynamic group chat, and a chair (LLM) picks who speaks next each turn.

---

## ⚙️ How It Works

```
        Admin presents a patient case
                    │
                    ▼
        ┌───────────────────────────┐
        │   SelectorGroupChat        │  ← LLM chair picks next speaker
        │                            │
        │  Kinesiology ⇄ Psychologist│
        │       ⇅            ⇅        │
        │  Data Analyst ⇄ Safety      │
        └───────────────────────────┘
                    │
                    ▼
   Unified protocol  →  Safety Auditor: APPROVED ✅
```

- **Dynamic discussion** via `SelectorGroupChat` (not a fixed pipeline).
- **Grounded in real science**: the Kinesiology Expert calls `assess_athlete`,
  which computes the Acute:Chronic Workload Ratio (ACWR) and a risk score —
  deterministic, never guessed.
- **Safe termination**: stops on `APPROVED` or a max-message cap (no infinite loops).

---

## 🛠️ Tech Stack

- **AutoGen v0.4** (`autogen-agentchat`, `autogen-ext`) — multi-agent teams
- **OpenRouter** — LLM access
- Deterministic Python tools reused from my
  [injury-risk-predictor](https://github.com/Hamzadatablok/injury-risk-predictor) project

---

## 🚀 Quick Start

```bash
python -m venv venv
venv\Scripts\activate              # Windows
pip install -r requirements.txt
copy .env.example .env             # add your OpenRouter key
python main.py
```

---

## 📂 Structure

| File | Role |
|------|------|
| `science.py` | Deterministic tools: ACWR, risk, combined `assess_athlete` |
| `agents.py` | The four committee agents + model client |
| `committee.py` | Assembles the agents into a SelectorGroupChat |
| `main.py` | Entry point — presents a case and runs the discussion |

---

## ⚠️ Disclaimer

This is an educational project, not a medical diagnostic tool.

## 👤 Author

**Hamza Elouahdani** — Data Scientist & Sports Performance Specialist
