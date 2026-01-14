from typing import Dict, List, Tuple
from .db import connect

def add_transaction(user_id: int, t_type: str, date: str, category: str, amount: float, note: str = "") -> None:
    with connect() as conn:
        conn.execute(
            "INSERT INTO transactions (user_id, type, date, category, amount, note) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, t_type, date, category, amount, note),
        )

def list_transactions(user_id: int, year_month: str) -> List[Tuple]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT date, type, category, amount, note
            FROM transactions
            WHERE user_id = ? AND substr(date, 1, 7) = ?
            ORDER BY date ASC
            """,
            (user_id, year_month),
        ).fetchall()
    return rows

def set_budget(user_id: int, year_month: str, category: str, limit_amount: float) -> None:
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO budgets (user_id, year_month, category, limit_amount)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, year_month, category)
            DO UPDATE SET limit_amount = excluded.limit_amount
            """,
            (user_id, year_month, category, limit_amount),
        )

def get_budgets(user_id: int, year_month: str) -> Dict[str, float]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT category, limit_amount FROM budgets WHERE user_id = ? AND year_month = ?",
            (user_id, year_month),
        ).fetchall()
    return {cat: float(lim) for cat, lim in rows}

def monthly_summary(user_id: int, year_month: str) -> Dict:
    with connect() as conn:
        income = conn.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE user_id = ? AND substr(date, 1, 7) = ? AND type = 'income'
            """,
            (user_id, year_month),
        ).fetchone()[0]

        expense = conn.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE user_id = ? AND substr(date, 1, 7) = ? AND type = 'expense'
            """,
            (user_id, year_month),
        ).fetchone()[0]

        by_category = conn.execute(
            """
            SELECT category, COALESCE(SUM(amount), 0) AS total
            FROM transactions
            WHERE user_id = ? AND substr(date, 1, 7) = ? AND type = 'expense'
            GROUP BY category
            ORDER BY total DESC
            """,
            (user_id, year_month),
        ).fetchall()

    return {
        "income": float(income),
        "expense": float(expense),
        "net": float(income) - float(expense),
        "by_category": [(c, float(t)) for c, t in by_category],
    }

def budget_alerts(user_id: int, year_month: str, threshold: float = 0.8) -> List[str]:
    budgets = get_budgets(user_id, year_month)
    if not budgets:
        return []

    summary = monthly_summary(user_id, year_month)
    spent_map = {cat: total for cat, total in summary["by_category"]}

    alerts: List[str] = []
    for cat, limit_amt in budgets.items():
        if limit_amt <= 0:
            continue

        spent = spent_map.get(cat, 0.0)
        ratio = spent / limit_amt

        if ratio >= 1.0:
            alerts.append(f"OVER BUDGET: {cat} spent {spent:.2f} / limit {limit_amt:.2f}")
        elif ratio >= threshold:
            alerts.append(f"WARNING: {cat} spent {spent:.2f} / limit {limit_amt:.2f} ({ratio*100:.0f}%)")

    return alerts
