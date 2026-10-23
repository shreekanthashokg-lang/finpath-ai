"""Rule-based copilot. Runs fully offline.
If OPENAI_API_KEY is set, it can optionally use an LLM — but all
financial figures ALWAYS come from src/calculator.py, never the LLM."""
import os, re
from src.calculator import emi

JARGON = {
  "EMI": "Equated Monthly Instalment — the fixed amount you pay every month until the loan is fully repaid. Part of it repays the loan, part is interest.",
  "Interest Rate (APR)": "The yearly cost of borrowing, as a percentage of the loan. Lower is better — always compare APR, not just the monthly rate.",
  "Principal": "The actual amount you borrow. Interest is calculated on this (in reducing-balance loans, on whatever principal is still unpaid).",
  "Tenure": "How long you take to repay — in months or years. Longer tenure = smaller EMI but MORE total interest.",
  "Processing Fee": "A one-time charge for giving you the loan, usually 0.5–3% of the amount. Ask for it in writing before signing.",
  "Foreclosure": "Closing your loan early by paying everything at once. Some lenders charge a penalty for this — check first.",
  "Prepayment": "Paying an extra chunk of your loan before it's due. It reduces your principal and saves interest.",
  "CIBIL Score": "A 300–900 score summarising your repayment history. Above 700 usually gets better rates.",
  "Reducing Balance": "Interest is charged only on the money you still owe — not the original amount. Most fair modern loans work this way.",
  "NPA": "Non-Performing Asset — a loan where repayments have stopped for 90+ days. Stay far away from this status.",
  "Eligibility Criteria": "The conditions you must meet (income, age, documents, credit score) before a lender will consider your application.",
  "Sanction Letter": "The official document saying your loan is approved, with the exact amount, rate and terms. Read it fully before accepting.",
}

DOCS = [
  ("PAN Card", "required", "Identity proof — must match your name exactly"),
  ("Address Proof", "required", "Aadhaar / passport / utility bill (any one)"),
  ("Last 3 Months' Bank Statements", "required", "Shows income and spending patterns"),
  ("Salary Slips (last 3 months)", "required", "For salaried applicants"),
  ("ITR / Form 16 (last year)", "optional", "Strengthens your file; often needed for bigger loans"),
  ("Passport-size Photograph", "required", "Recent, clear background"),
  ("Existing Loan Statements", "conditional", "Only if you already have another loan"),
]

_RULES = [
  (r"\b(emi|installment|monthly payment)\b", "emi"),
  (r"\b(afford|budget|repay)\b", "afford"),
  (r"\b(documents?|papers?|kyc|checklist)\b", "docs"),
  (r"\b(compare|option|which loan|best)\b", "compare"),
  (r"\b(cibil|credit score)\b", "cibil"),
  (r"\b(interest|rate)\b", "rate"),
  (r"\b(next|what now|step)\b", "next"),
  (r"\b(hi|hello|hey|namaste)\b", "greet"),
]

def get_response(text: str, ctx: dict) -> str:
    t = text.lower()
    for pat, tag in _RULES:
        if re.search(pat, t):
            return _REPLY[tag](ctx)
    return ("I can help with: EMI & affordability, documents needed, comparing loan options, "
            "or explaining any financial term (try: 'what is foreclosure?').")


def _g(ctx): return "Namaste! Tell me your goal — for example: 'I need a ₹1,00,000 loan. Can I afford it?'"

def _emi(ctx):
    c = ctx.get("calc")
    if not c: return ("Let's calculate. Head to the Journey tab and enter the loan amount, interest rate and tenure — "
                      "I'll show the exact EMI and total cost instantly.")
    return (f"For your loan: EMI is ₹{c['emi']:,.0f} per month. Total repayment ₹{c['total_repayment']:,.0f} "
            f"of which interest is ₹{c['total_interest']:,.0f}. Figures are estimates — actual lender terms may differ.")

def _afford(ctx):
    a = ctx.get("afford")
    if not a: return "Enter your income and expenses in the Journey tab and I'll assess affordability honestly — no sugar-coating."
    return f"Assessment: {a['status']} — {a['message']}"

def _docs(ctx): return "Typical documents: " + "; ".join(d[0] for d in DOCS if d[1] in ("required","conditional")) +                       ". The Documents tab gives you a live checklist."

def _compare(ctx): return "Open the Compare tab — three synthetic products are side-by-side on rate, fees and eligibility. Real product terms must be verified with the lender."

def _cibil(ctx): return JARGON["CIBIL Score"]

def _rate(ctx): return JARGON["Interest Rate (APR)"] + " Tip: a 1% lower APR on a ₹1L/12-month loan saves you roughly ₹550 in interest."

def _next(ctx):
    done = ctx.get("steps", set())
    if "affordability" not in done: return "Step 1 — complete the affordability check in the Journey tab."
    if "documents" not in done: return "Step 2 — finish your document checklist in the Documents tab."
    if "compare" not in done: return "Step 3 — compare products in the Compare tab."
    return "You're decision-ready. Review estimates vs verified terms, then apply with the lender of your choice. FinPath AI never promises approval — lenders decide."

_REPLY = {"greet": _g, "emi": _emi, "afford": _afford, "docs": _docs,
          "compare": _compare, "cibil": _cibil, "rate": _rate, "next": _next}


def explain_term(term: str):
    return JARGON.get(term, "Term not in dictionary yet.")
