import json
import os
from datetime import date, timedelta
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Demo data only. Replace these records with database queries before real use.
TODAY = date(2026, 10, 11)

TRANSACTIONS = [
    {"date": "2026-10-05", "order_id": "B001", "product": "Classic Hoodie", "qty": 2, "unit_price": 4200, "unit_cost": 2600, "delivery": 400, "packaging": 100, "other_expense": 0},
    {"date": "2026-10-05", "order_id": "B002", "product": "Canvas Tote", "qty": 3, "unit_price": 1200, "unit_cost": 650, "delivery": 300, "packaging": 90, "other_expense": 0},
    {"date": "2026-10-06", "order_id": "B003", "product": "Classic Hoodie", "qty": 1, "unit_price": 4200, "unit_cost": 2600, "delivery": 400, "packaging": 50, "other_expense": 0},
    {"date": "2026-10-07", "order_id": "B004", "product": "Everyday Sneakers", "qty": 1, "unit_price": 6800, "unit_cost": 4300, "delivery": 500, "packaging": 100, "other_expense": 0},
    {"date": "2026-10-08", "order_id": "B005", "product": "Canvas Tote", "qty": 2, "unit_price": 1200, "unit_cost": 650, "delivery": 300, "packaging": 60, "other_expense": 0},
    {"date": "2026-10-09", "order_id": "B006", "product": "Classic Hoodie", "qty": 2, "unit_price": 4200, "unit_cost": 2600, "delivery": 400, "packaging": 100, "other_expense": 0},
    {"date": "2026-10-10", "order_id": "B007", "product": "Everyday Sneakers", "qty": 1, "unit_price": 6800, "unit_cost": 4300, "delivery": 500, "packaging": 100, "other_expense": 0},
    {"date": "2026-10-11", "order_id": "B008", "product": "Canvas Tote", "qty": 4, "unit_price": 1200, "unit_cost": 650, "delivery": 350, "packaging": 120, "other_expense": 0},
]

OVERHEAD_EXPENSES = [
    {"date": "2026-10-06", "label": "Internet", "amount": 1200},
    {"date": "2026-10-09", "label": "Promotion", "amount": 1800},
]

INVENTORY = [
    {"product": "Classic Hoodie", "sku": "HD-001", "stock": 4, "reorder_level": 5, "unit_cost": 2600},
    {"product": "Canvas Tote", "sku": "TB-002", "stock": 18, "reorder_level": 6, "unit_cost": 650},
    {"product": "Everyday Sneakers", "sku": "SN-003", "stock": 2, "reorder_level": 4, "unit_cost": 4300},
    {"product": "Minimal Wallet", "sku": "WL-004", "stock": 9, "reorder_level": 4, "unit_cost": 900},
]

def _period_start(period: str) -> date:
    p = period.strip().lower()
    if p in {"today", "day"}:
        return TODAY
    if p in {"week", "this week", "weekly"}:
        return TODAY - timedelta(days=6)
    if p in {"month", "this month", "monthly"}:
        return TODAY.replace(day=1)
    return date(1900, 1, 1)

def _filter_transactions(period: str):
    start = _period_start(period)
    return [t for t in TRANSACTIONS if start <= date.fromisoformat(t["date"]) <= TODAY]

def _money(value: float) -> str:
    return f"{value:,.0f} DZD"

@tool
def get_sales(period: Literal["today", "week", "month", "all"] = "week") -> str:
    """Get recorded sales totals and best-selling products for today, this week, this month, or all demo records."""
    rows = _filter_transactions(period)
    if not rows:
        return f"No sales records found for period '{period}'."
    revenue_by_product = {}
    for row in rows:
        revenue_by_product[row["product"]] = revenue_by_product.get(row["product"], 0) + row["qty"] * row["unit_price"]
    total_revenue = sum(r["qty"] * r["unit_price"] for r in rows)
    total_units = sum(r["qty"] for r in rows)
    best = max(revenue_by_product, key=revenue_by_product.get)
    return json.dumps({
        "period": period,
        "orders": len(rows),
        "units_sold": total_units,
        "revenue_dzd": total_revenue,
        "revenue_formatted": _money(total_revenue),
        "sales_by_product_dzd": revenue_by_product,
        "best_selling_product_by_revenue": best,
        "note": "Demo data only; these are example transactions, not real business records."
    }, ensure_ascii=False)

@tool
def calculate_profit(period: Literal["today", "week", "month", "all"] = "week") -> str:
    """Calculate estimated profit for today, this week, this month, or all demo records. Include product costs, delivery, packaging, and dated overhead expenses. Revenue is not profit."""
    rows = _filter_transactions(period)
    start = _period_start(period)
    overhead = sum(e["amount"] for e in OVERHEAD_EXPENSES if start <= date.fromisoformat(e["date"]) <= TODAY)
    revenue = sum(r["qty"] * r["unit_price"] for r in rows)
    cogs = sum(r["qty"] * r["unit_cost"] for r in rows)
    delivery = sum(r["delivery"] for r in rows)
    packaging = sum(r["packaging"] for r in rows)
    total_costs = cogs + delivery + packaging + overhead
    profit = revenue - total_costs
    return json.dumps({
        "period": period,
        "revenue_dzd": revenue,
        "product_costs_dzd": cogs,
        "delivery_costs_dzd": delivery,
        "packaging_costs_dzd": packaging,
        "other_expenses_dzd": overhead,
        "total_recorded_costs_dzd": total_costs,
        "estimated_profit_dzd": profit,
        "profit_margin_percent": round((profit / revenue * 100), 1) if revenue else None,
        "revenue_formatted": _money(revenue),
        "estimated_profit_formatted": _money(profit),
        "assumptions": "Estimated profit = recorded sales revenue minus listed product, delivery, packaging, and overhead costs. Taxes, returns, unpaid orders, and missing expenses are not included.",
        "note": "Demo data only; these are example transactions, not real business records."
    }, ensure_ascii=False)

@tool
def check_stock() -> str:
    """Check current demo inventory and identify products at or below their reorder level."""
    low_stock = [item for item in INVENTORY if item["stock"] <= item["reorder_level"]]
    return json.dumps({
        "inventory": INVENTORY,
        "low_stock_products": low_stock,
        "low_stock_count": len(low_stock),
        "note": "Demo inventory only; stock figures are examples, not live shop inventory."
    }, ensure_ascii=False)

system_prompt = """
You are Businessy, a practical AI assistant for small Algerian businesses.
You can help with three tasks:
1. Profit analysis using calculate_profit.
2. Inventory and restocking using check_stock.
3. Sales summaries using get_sales.

Rules:
- Use the tools for all numerical answers about sales, costs, profit, and stock.
- Never invent or estimate figures that are not returned by tools.
- Always distinguish revenue (sales) from profit.
- State that figures are demo data when relevant, and do not imply this is connected to a real shop.
- Report money in DZD (Algerian dinars).
- Explain calculations in clear, friendly language. If a user asks about a period, pass the closest supported period: today, week, month, or all.
- If costs are missing or a calculation is only partial, say so explicitly.
- Do not perform purchases, send messages, or modify records; this prototype is read-only.
"""

model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
model = ChatGoogleGenerativeAI(model=model_name, temperature=0.1)
agent = create_agent(
    model=model,
    tools=[get_sales, calculate_profit, check_stock],
    system_prompt=system_prompt,
)

# LangGraph Agent Chat UI expects a graph named in langgraph.json.
graph = agent
