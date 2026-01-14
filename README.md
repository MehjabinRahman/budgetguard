# BudgetGuard – Advanced Python Expense & Budget Tracker

BudgetGuard is an advanced, console-based Python application designed to manage personal finances efficiently.  
It supports **multiple users**, **secure authentication**, **SQLite database storage**, **monthly budgets**, and **automatic budget alerts**, all through a clean command-line interface.

This project is intended for **GitHub portfolios**, **Computer Science resumes**, and **technical interviews**, demonstrating backend development, data persistence, and structured Python design.

---

## Features

- Multi-user system (user signup and login)
- Passwords stored using **hashed and salted encryption**
- Store income and expenses in a **SQLite database**
- Track transactions by date, category, amount, and notes
- Monthly financial summary (total income, expenses, and net balance)
- Category-wise expense breakdown
- Set **monthly budget limits per category**
- Automatic **budget alerts** when nearing or exceeding limits
- Clean and readable command-line interface

---

## Technologies Used

- **Python 3**
- SQLite (`sqlite3`)
- Typer (command-line framework)
- Rich (formatted terminal output)
- Hashlib (password hashing)
- Modular Python package structure

---

## Installation & Setup

Install required dependencies:
pip install -r requirements.txt

---

How to Run the Application
1. Initialize the database
python -m src.budgetguard.main init

2. Create a new user account
python -m src.budgetguard.main signup USERNAME PASSWORD

3. Log in
python -m src.budgetguard.main signin USERNAME PASSWORD

---

Usage Examples
1. Add an expense
python -m src.budgetguard.main add --t-type expense --category Food --amount 25.50 --note "Lunch"

2. Add income
python -m src.budgetguard.main add --t-type income --category Salary --amount 1500

3. Set a monthly budget
python -m src.budgetguard.main budget 2026-01 Food 300

4. View monthly summary and budget alerts
python -m src.budgetguard.main summary 2026-01

5. View transactions for a month
python -m src.budgetguard.main show 2026-01




