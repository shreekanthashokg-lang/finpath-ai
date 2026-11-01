# 🧭 FinPath AI — Your Financial Journey Co-Pilot

**Track 2: AI-Powered Financial Journeys** · Paytm Build for India AI Hackathon — Bengaluru Edition

> Chatbots answer. FinPath AI walks the journey with you — and helps you finish it.

FinPath AI transforms confusing financial processes (starting with **loan readiness**) into a
guided, transparent, step-by-step journey: conversational intake → deterministic affordability
analysis → plain-language explanations → document readiness checklist → transparent comparison →
confident decision.

## ✨MVP HACKTHON FEATURES

| Feature | What it does |
|---|---|
| 🎯 Guided Loan Journey | Goal → affordability → documents → comparison → decision, with a live journey tracker |
| 🧮 Deterministic Affordability Engine | Reducing-balance EMI, total interest, budget-pressure ratios — **pure Python, never LLM-generated** |
| 📖 Jargon Translator | 12 financial terms explained in plain language (ELI5) |
| 📄 Document Readiness Assistant | Personalized checklist with live progress |
| 📊 Transparent Comparison | Synthetic products side-by-side on rate, fees, eligibility |
| 💬 Offline Copilot | Rule-based assistant that knows your journey context — **zero API keys required** |
| 🛡️ Trust by Design | Estimates ≠ verified terms ≠ lender decisions. Never promises approval. |

## 🏗️ Architecture

```
Streamlit UI (tabs + journey tracker)
        │
FastAPI-ready backend (src/)
        ├── calculator.py   ← deterministic EMI / affordability math (auditable)
        └── copilot.py      ← rule-based dialogue + jargon dictionary + context
Data: data/products.json    ← synthetic demo products only
```

**Design rule:** all numbers come from `src/calculator.py`. The AI (present/future LLM layer)
only *explains* numbers — it never *computes* them.

## 🚀 Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ DEPLOYED ON STEAMLIT COMMUNITY CLOUD

1. Push this repo to GitHub (see below).
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Pick your repo, set **Main file path = `app.py`**, click **Deploy**.
4. Done — you get a public URL like `https://your-app.streamlit.app`.

## 📤 Push to GitHub

```bash
git init
git add .
git commit -m "FinPath AI — hackathon MVP: loan journey, affordability engine, checklist, comparison"
git branch -M main
git remote add origin https://github.com/<your-username>/finpath-ai.git
git push -u origin main
```

## ⚠️ Disclaimers

- All products, rates and figures are **synthetic demo data**.
- Outputs are **estimates**, not financial advice, not verified product terms, and **not loan approvals**.
- Actual lending decisions rest solely with licensed lenders.
- Built for a hackathon with consent-first, explainable-AI principles (DPDP-aware by design).

## 🗺️ Roadmap

- [ ] LLM dialogue layer (optional, OpenAI-compatible) with RAG over verified product docs
- [ ] OCR document upload → auto-fill with user confirmation
- [ ] Voice input in Hindi + regional languages
- [ ] Insurance claim-guidance journey
- [ ] Paytm sandbox API integration

---
BUILT WITH ❤️ FOR THE PAYTM BUILD FOR INDIA AI HACKTHON, Bengaluru — 31 Oct 2026.
