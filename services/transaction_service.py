from models import Transaction


def calculate_summary(data):
    income = sum(r.amount for r in data if r.type == "income")
    expense = sum(r.amount for r in data if r.type == "expense")

    return {
        "total_income": income,
        "total_expense": expense,
        "balance": income - expense
    }


def category_analysis(data):
    result = {}

    for r in data:
        if r.type == "expense":
            result[r.category] = result.get(r.category, 0) + r.amount

    return result