"""Deterministic financial engine. NEVER use an LLM for numbers.
All functions are pure, unit-testable, and auditable."""
import numpy as np


def emi(principal: float, annual_rate_pct: float, tenure_months: int) -> dict:
    """Standard reducing-balance EMI (monthly rests)."""
    if tenure_months <= 0 or principal <= 0:
        raise ValueError("Principal and tenure must be positive.")
    r = annual_rate_pct / 100 / 12
    if r == 0:
        e = principal / tenure_months
    else:
        e = principal * r * (1 + r) ** tenure_months / ((1 + r) ** tenure_months - 1)
    total = e * tenure_months
    return {
        "emi": round(e, 2),
        "total_repayment": round(total, 2),
        "total_interest": round(total - principal, 2),
        "monthly_rate": round(r, 6),
    }


def affordability(emi_val: float, monthly_income: float, monthly_expenses: float) -> dict:
    surplus = monthly_income - monthly_expenses
    if surplus <= 0:
        return {"status": "RISK", "emi_to_income_pct": round(emi_val / monthly_income * 100, 1),
                "emi_to_surplus_pct": None, "buffer": round(-surplus, 2),
                "message": "Expenses already exceed income. Any new EMI would add debt stress."}
    ei = emi_val / monthly_income * 100
    es = emi_val / surplus * 100
    buffer = surplus - emi_val
    status = "COMFORTABLE" if es < 70 else ("TIGHT" if es < 90 else "RISKY")
    return {"status": status, "emi_to_income_pct": round(ei, 1),
            "emi_to_surplus_pct": round(es, 1), "buffer": round(buffer, 2),
            "surplus": round(surplus, 2),
            "message": {
                "COMFORTABLE": "EMI fits comfortably within your budget with room to spare.",
                "TIGHT": "EMI is payable but leaves little room for surprises — consider a longer tenure.",
                "RISKY": "EMI consumes most of your spare money. A smaller amount or longer tenure is safer.",
                "RISK": "Do not take this loan until expenses are restructured.",
            }[status]}


def amortization_schedule(principal, annual_rate_pct, tenure_months):
    r = annual_rate_pct / 100 / 12
    e = emi(principal, annual_rate_pct, tenure_months)["emi"]
    bal, rows = principal, []
    for m in range(1, tenure_months + 1):
        interest = bal * r
        principal_paid = e - interest
        bal -= principal_paid
        rows.append({"Month": m, "EMI": round(e, 2), "Interest": round(interest, 2),
                     "Principal": round(principal_paid, 2), "Balance": round(max(bal, 0), 2)})
    return rows
