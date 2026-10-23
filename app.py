"""
FinPath AI — Financial Journey Co-Pilot
Track 2: AI-Powered Financial Journeys | Paytm Build for India AI Hackathon — Bengaluru
All data is SYNTHETIC. Figures are estimates, never approvals. Lenders make all decisions.
"""
import json
import streamlit as st
import pandas as pd

from src.calculator import emi, affordability, amortization_schedule
from src.copilot import JARGON, DOCS, get_response

st.set_page_config(page_title="FinPath AI", page_icon="🧭", layout="wide")

# ── session state ──────────────────────────────
for k, v in [("steps", set()), ("chat", []), ("docs_done", set()), ("calc", None), ("afford", None)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── sidebar: journey tracker ───────────────────
STEPS = ["goal", "affordability", "documents", "compare", "decision"]
LABELS = {"goal": "🎯 State your goal", "affordability": "🧮 Affordability check",
          "documents": "📄 Document readiness", "compare": "📊 Compare options",
          "decision": "✅ Confident decision"}
with st.sidebar:
    st.title("🧭 FinPath AI")
    st.caption("From confusion to confident completion.")
    st.divider()
    st.subheader("Journey Tracker")
    for s_ in STEPS:
        mark = "✅" if s_ in st.session_state.steps else "⬜"
        st.write(f"{mark} {LABELS[s_]}")
    st.progress(len(st.session_state.steps) / len(STEPS))
    if st.button("↺ Reset journey", use_container_width=True):
        st.session_state.steps, st.session_state.docs_done = set(), set()
        st.session_state.calc = st.session_state.afford = None
        st.session_state.chat = []
        st.rerun()
    st.divider()
    st.caption("⚠️ All products & figures are **synthetic demo data**. "
               "Estimates ≠ verified terms ≠ lender decisions. FinPath AI never promises approval.")

# ── header ─────────────────────────────────────
st.title("🧭 FinPath AI — Your Financial Journey Co-Pilot")
st.markdown("**Track 2: AI-Powered Financial Journeys** · Paytm Build for India AI Hackathon, Bengaluru")
st.info("💡 Try the demo journey: state a goal → check affordability → finish documents → compare → decide. "
        "Everything runs locally with deterministic, auditable math.", icon="🚀")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🎯 Journey", "📄 Documents", "📊 Compare", "💬 Copilot", "📖 Jargon Translator"])

# ═══ TAB 1: JOURNEY ═══
with tab1:
    colA, colB = st.columns([1, 1.2])
    with colA:
        st.subheader("Tell us your goal")
        goal = st.text_input("Your goal", value="I need a personal loan of ₹1,00,000. Can I afford it?")
        c1, c2 = st.columns(2)
        income = c1.number_input("Monthly income (₹)", min_value=0, value=35000, step=1000)
        expenses = c2.number_input("Monthly expenses (₹)", min_value=0, value=20000, step=1000)
        c3, c4, c5 = st.columns(3)
        amount = c3.number_input("Loan amount (₹)", min_value=1000, value=100000, step=10000)
        rate = c4.number_input("Interest rate (% p.a.)", min_value=0.0, value=12.0, step=0.5)
        tenure = c5.number_input("Tenure (months)", min_value=1, value=12, step=6)
        if st.button("🔍 Analyse my loan", type="primary", use_container_width=True):
            try:
                calc = emi(amount, rate, tenure)
                aff = affordability(calc["emi"], income, expenses)
                st.session_state.calc, st.session_state.afford = calc, aff
                st.session_state.steps.update(["goal", "affordability"])
                st.rerun()
            except ValueError as e:
                st.error(str(e))
    with colB:
        if st.session_state.calc:
            c = st.session_state.calc; a = st.session_state.afford
            m1, m2, m3 = st.columns(3)
            m1.metric("EMI / month", f"₹{c['emi']:,.0f}")
            m2.metric("Total interest", f"₹{c['total_interest']:,.0f}")
            m3.metric("Total repayment", f"₹{c['total_repayment']:,.0f}")
            color = {"COMFORTABLE": "green", "TIGHT": "orange", "RISKY": "red", "RISK": "red"}[a["status"]]
            st.markdown(f":{color}[**Affordability: {a['status']}** — {a['message']}]")
            if a.get("emi_to_surplus_pct") is not None:
                st.caption(f"EMI = {a['emi_to_income_pct']}% of income · "
                           f"{a['emi_to_surplus_pct']}% of your monthly surplus (₹{a['surplus']:,.0f}) · "
                           f"buffer left: ₹{a['buffer']:,.0f}/month")
            with st.expander("📅 Amortization schedule"):
                st.dataframe(pd.DataFrame(amortization_schedule(amount, rate, tenure)),
                             use_container_width=True, height=220)
            st.caption("⚠️ Estimate based on reducing-balance method. Actual lender rates, fees and terms may differ.")
        else:
            st.info("Fill the form and press **Analyse my loan** — the math is deterministic and auditable, never LLM-generated.", icon="🧮")

# ═══ TAB 2: DOCUMENTS ═══
with tab2:
    st.subheader("Document Readiness Checklist")
    st.caption("Check items off as you gather them. (OCR auto-fill integrates in the full build — demo uses manual checklist.)")
    for name, req, why in DOCS:
        done = st.checkbox(f"**{name}**  `{req}` — {why}", key=f"doc_{name}")
        if done:
            st.session_state.docs_done.add(name)
        else:
            st.session_state.docs_done.discard(name)
    n, total = len(st.session_state.docs_done), len(DOCS)
    st.progress(n / total, text=f"{n}/{total} documents ready")
    if n >= sum(1 for d in DOCS if d[1] in ("required", "conditional")):
        st.session_state.steps.add("documents")
        st.success("📄 All required documents ready! Journey step completed.")
    st.divider()
    up = st.file_uploader("Upload a document (demo — nothing is stored or sent anywhere)",
                          type=["pdf", "jpg", "png"])
    if up:
        st.success(f"Received **{up.name}** ({up.size/1024:.1f} KB). In production, OCR would extract and auto-fill form fields after your confirmation.")

# ═══ TAB 3: COMPARE ═══
with tab3:
    st.subheader("Compare Options — transparent, side-by-side")
    products = json.load(open("data/products.json"))
    df = pd.DataFrame(products)
    df["processing_fee_pct"] = df["processing_fee_pct"].astype(str) + "%"
    df["rate"] = df["rate"].astype(str) + "% p.a."
    st.dataframe(df[["name", "type", "rate", "processing_fee_pct", "tenure_months",
                     "min_income", "max_amount", "features"]],
                 use_container_width=True, hide_index=True)
    st.caption("⚠️ **Synthetic demo products.** Real comparisons must use verified, current lender terms. "
               "Sponsored placement, if any, will always be disclosed.")
    if st.button("✅ I've compared my options", use_container_width=False):
        st.session_state.steps.add("compare")
        st.success("Comparison noted. Now make your confident decision — the final step!")

# ═══ TAB 4: COPILOT ═══
with tab4:
    st.subheader("💬 Journey Copilot (runs fully offline)")
    st.caption("Ask about EMI, affordability, documents, comparisons, or your next step.")
    for role, msg in st.session_state.chat:
        with st.chat_message(role):
            st.markdown(msg)
    prompt = st.chat_input("e.g. 'What is my EMI?' or 'what documents do I need?'")
    if prompt:
        st.session_state.chat.append(("user", prompt))
        ctx = {"calc": st.session_state.calc, "afford": st.session_state.afford,
               "steps": st.session_state.steps}
        reply = get_response(prompt, ctx)
        st.session_state.chat.append(("assistant", reply))
        st.rerun()
    if len(st.session_state.steps) >= 4 and "decision" not in st.session_state.steps:
        st.session_state.steps.add("decision")
    if "decision" in st.session_state.steps:
        st.balloons()
        st.success("🎉 Journey complete — you moved from confusion to a confident decision. FinPath AI guided; you decided.")

# ═══ TAB 5: JARGON ═══
with tab5:
    st.subheader("📖 Financial Jargon Translator — explained like a friend would")
    term = st.selectbox("Pick a term", sorted(JARGON.keys()))
    st.info(f"**{term}** — {JARGON[term]}", icon="💡")
    st.caption("Understanding first, paperwork second. That's the FinPath AI way.")
