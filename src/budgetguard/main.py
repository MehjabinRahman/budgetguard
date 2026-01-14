from datetime import datetime
import typer
from rich.console import Console
from rich.table import Table

from .db import init_db
from .auth import register, login
from .services import add_transaction, list_transactions, monthly_summary, set_budget, budget_alerts

app = typer.Typer(help="BudgetGuard - Advanced Python Expense & Budget Tracker")
console = Console()

SESSION = {"user_id": None, "username": None}

def require_login():
    if SESSION["user_id"] is None:
        console.print("[red]You must login first.[/red]")
        raise typer.Exit(code=1)

@app.command()
def init():
    """Initialize the SQLite database."""
    init_db()
    console.print("[green]Database initialized.[/green]")

@app.command()
def signup(username: str, password: str):
    """Create a new account."""
    init_db()
    if register(username, password):
        console.print("[green]Account created. Now sign in.[/green]")
    else:
        console.print("[red]Username already exists or an error occurred.[/red]")

@app.command()
def signin(username: str, password: str):
    """Sign in to an existing account."""
    init_db()
    user_id = login(username, password)
    if user_id is None:
        console.print("[red]Invalid username or password.[/red]")
        raise typer.Exit(code=1)

    SESSION["user_id"] = user_id
    SESSION["username"] = username
    console.print(f"[green]Logged in as {username}[/green]")

@app.command()
def add(
    t_type: str = typer.Option(..., "--t-type", help="income or expense"),
    date: str = typer.Option("", help="YYYY-MM-DD (blank = today)"),
    category: str = typer.Option(..., help="Category name (e.g., Food, Rent)"),
    amount: float = typer.Option(..., help="Positive number"),
    note: str = typer.Option("", help="Optional note"),
):
    """Add a transaction."""
    require_login()

    if t_type not in ("income", "expense"):
        console.print("[red]--t-type must be 'income' or 'expense'[/red]")
        raise typer.Exit(code=1)

    if not date:
        date = datetime.today().strftime("%Y-%m-%d")

    add_transaction(SESSION["user_id"], t_type, date, category, amount, note)
    console.print("[green]Saved transaction.[/green]")

@app.command()
def show(month: str = typer.Argument(..., help="YYYY-MM")):
    """Show all transactions for a month."""
    require_login()
    rows = list_transactions(SESSION["user_id"], month)

    table = Table(title=f"Transactions for {month}")
    table.add_column("Date")
    table.add_column("Type")
    table.add_column("Category")
    table.add_column("Amount", justify="right")
    table.add_column("Note")

    for d, t, c, a, n in rows:
        table.add_row(d, t, c, f"{_
