import json
import csv
from datetime import datetime
import argparse


def load_expenses():
    try:
        with open("expenses.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Could not find 'expenses.json'")
        return []
    except json.JSONDecodeError:
        raise ValueError("Invalid or corrupted JSON file")

def save_expenses(expenses):
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)

def add_expense(expenses, description,
                 amount, category, date):
    highest_id = 0
    validate_amount(amount)
    validate_date(date)
    if description.isdigit() is True:
        raise ValueError("Please enter a valid description of your item.")
    if category.isdigit() is True:
        raise ValueError("Please enter a valid name for your category.")

    for expense in expenses:
        if expense["id"] > highest_id:
            highest_id = expense["id"]
    expense_id = highest_id+1
    new_expense = {"id": expense_id, "description": description, 
                "amount": amount, 
                "category": category,"date": date}

    expenses.append(new_expense)
    save_expenses(expenses)
    print(f"Successfully added {new_expense['description']}")

def view_expenses(expenses):
        if not expenses:
            print("No expenses found.")
            return
        for expense in expenses:
            print(f"ID: {expense['id']}")
            print(f"Description: {expense['description']}")
            print(f"Amount: {expense['amount']}")
            print(f"Category: {expense['category']}")
            print(f"Date: {expense['date']}")
            print()

def delete_expense(expenses, expense_id):
    if not expenses:
        print("No expenses found.")
        return
    for expense in expenses:
        if expense['id'] == expense_id:
            expenses.remove(expense)
            save_expenses(expenses)
            print("Expense removed.")
            return
    else:
        print(f"Could not find any expenses with ID: {expense_id}")

def update_expense(expenses, expense_id, description=None,
                 amount=None, category=None, date=None):
    for expense in expenses:
            if expense["id"] == expense_id:
                if all(value is None for value in [description, amount, 
                                                   category, date]):
                    print("No update fields were provided.")
                    return
                if not description is not None:
                    expense['description'] = description
                if not amount is not None:
                    validate_amount(amount)
                    expense['amount'] = amount
                if not category is not None:
                    expense['category'] = category
                if not date is not None:
                    validate_date(date)
                    expense['date'] = date
                save_expenses(expenses)
                print("Successfully updated expenses.")
                return expense
    else:
        print("Could not find any expense with this ID.")
            
def show_summary(expenses):
    if not expenses:
        print("No expenses found.")
        return
    total = sum(expense['amount'] for expense in expenses)  
    print (f"Total expenses: {total:.2f}")

def filter_by_category(expenses, category):
    found = False
    if not expenses:
        print("No expenses found.")
        return
    for expense in expenses:
        if expense['category'].lower() == category.lower():
            found = True
            print(f"ID: {expense['id']}")
            print(f"Description: {expense['description']}")
            print(f"Amount: {expense['amount']}")
            print(f"Category: {expense['category']}")
            print(f"Date: {expense['date']}")
            print()
    if not found:
        print("No expenses found under this category.")

def get_monthly_total(expenses, month):
    validate_month(month)
    current_year = datetime.now().year
    total = 0
    for expense in expenses:
        expense_date = datetime.strptime(expense["date"], "%Y-%m-%d")

        if expense_date.year == current_year and expense_date.month == month:
            total += expense["amount"]
    return total

def show_monthly_summary(expenses, month):
    total = get_monthly_total(expenses, month)
    print(f"Total amount spent: {total:.2f}")

def load_budgets():
    try:
        with open("budgets.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Could not find 'budgets.json'")
        return {}
    except json.JSONDecodeError:
        raise ValueError("Invalid or corrupted JSON file")

def save_budgets(budgets):
    with open("budgets.json", "w") as file:
        json.dump(budgets, file, indent=4)

def set_budget(budgets, month, amount):
    validate_month(month)
    validate_amount(amount)
    year= datetime.now().year
    key = f"{year}-{month:02d}"
    budgets[key] = amount
    save_budgets(budgets)
    print("Budget was successfully set.")

def check_budget(expenses, budgets, month):
    year= datetime.now().year
    key = f"{year}-{month:02d}"

    if key not in budgets:
        print("No budget was set for that month.")
        return
    total = get_monthly_total(expenses, month)
    budget = budgets[key]
    if total > budget:
        print(f"Warning: Monthly budget exceeded by {total-budget:.2f}")
    else:
        print(f"Remaining of the budget: {budget-total:.2f}")

def export_to_csv(expenses, filename):
    fieldnames=["id", "description", "amount", "category", "date"]
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses)
    print(f"successfully exported to csv: {filename}")

def validate_month(month):
    if month < 1 or month > 12:
        raise ValueError("The month must be between 1 and 12.")
def validate_amount(amount):
    if amount <=0:
        raise ValueError("Amount must be greater than zero.")
def validate_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must use 'YYYY-MM-DD' format.")

def create_parser():
    #parser
    parser = argparse.ArgumentParser(description="== Expenses Tracker ==")
    subparsers = parser.add_subparsers(dest="command")

    #add command
    add_parser = subparsers.add_parser("add", help=" Add a new expense.")
    add_parser.add_argument("--description", required=True)
    add_parser.add_argument("--amount", type=float, required=True)
    add_parser.add_argument("--category", required=True)
    add_parser.add_argument("--date")

    #delete command
    delete_parser = subparsers.add_parser("delete", help="Delete an expense.")
    delete_parser.add_argument("id", type=int)

    #summary command
    summary_parser = subparsers.add_parser("summary", help="Show expenses summary.")
    summary_parser.add_argument("--month", type=int)

    #update command
    update_parser = subparsers.add_parser("update", help="Update existing expenses.")
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("--description")
    update_parser.add_argument("--amount", type=float)
    update_parser.add_argument("--category")
    update_parser.add_argument("--date")

    #list command
    list_parser = subparsers.add_parser("list", help="List current expenses.")
    list_parser.add_argument("--category")

    #export command
    export_parser = subparsers.add_parser("export", help="Export expenses to a .csv file")
    export_parser.add_argument("--filename", required=True)

    #budget command
    budget_parser = subparsers.add_parser("budget", help="Set your budget for the month.")
    budget_parser.add_argument("--month", type=int, required=True)
    budget_parser.add_argument("--amount", type=float, required=True)
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        return

    try:
        expenses = load_expenses()
        budgets = load_budgets()

        if args.command == "add":
            if args.date is None:
                date = datetime.now().strftime("%Y-%m-%d")
            else:
                date = args.date
            add_expense(expenses, args.description,
                        args.amount, args.category,
                        date
            )
            expense_date = datetime.strptime(date, "%Y-%m-%d")
            month = expense_date.month
            check_budget(expenses, budgets, month)
        elif args.command == "delete":
            delete_expense(expenses, args.id)
        elif args.command == "summary":
            if args.month is None:
                show_summary(expenses)
            else:
                if validate_month(month):
                    print("Invalid Month")
                else:
                    show_monthly_summary(expenses, args.month)      
        elif args.command == "update":
            updated_expense = update_expense(expenses, args.id, args.description,
                        args.amount, args.category, args.date)
            if updated_expense is not None:
                expense_date = datetime.strptime(
                updated_expense["date"],"%Y-%m-%d")
                check_budget(expenses, budgets, expense_date.month)
        elif args.command == "list":
            if args.category is None:
                view_expenses(expenses)
            else:
                filter_by_category(expenses, args.category)
        elif args.command == "export":
            export_to_csv(expenses, args.filename)
        elif args.command == "budget":
            if args.month < 1 or args.month > 12:
                print("Invalid Month")
            else:
                set_budget(budgets, args.month, args.amount)
    except ValueError as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    main()