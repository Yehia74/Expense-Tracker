import unittest
from datetime import datetime
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout
from expenses_tracker import validate_amount, validate_month, validate_date, add_expense
from expenses_tracker import update_expense, delete_expense, get_monthly_total
from expenses_tracker import show_summary, filter_by_category, set_budget, check_budget

class TestValidators(unittest.TestCase):
    def test_negative_amount(self):
        with self.assertRaises(ValueError):
            validate_amount(-50)

    def test_zero_amount(self):
        with self.assertRaises(ValueError):
            validate_amount(0)

    def test_valid_amount(self):
        validate_amount(50)

    def test_invalid_month_1(self):
        with self.assertRaises(ValueError):
            validate_month(0)

    def test_invalid_month_2(self):
        with self.assertRaises(ValueError):
            validate_month(13)

    def test_valid_month(self):
        validate_month(9)

    def test_invalid_date_format(self):
        with self.assertRaises(ValueError):
            validate_date("13-10-2026")

    def test_invalid_date_value(self):
        with self.assertRaises(ValueError):
            validate_date("2026-13-10")

    def test_valid_date(self):
        validate_date("2026-09-10")

class TestAddExpense(unittest.TestCase):
    def test_add_expense(self):
        expenses = []
        with patch("expenses_tracker.save_expenses"):
            add_expense(expenses, "Doughnuts", 205, "Food", "2026-09-10")
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]['id'], 1)
        self.assertEqual(expenses[0]['description'], "Doughnuts")
        self.assertEqual(expenses[0]['amount'], 205)
        self.assertEqual(expenses[0]['category'], "Food")
        self.assertEqual(expenses[0]['date'], "2026-09-10")

    def test_correct_id_generation(self):
        expenses = [
    {"id": 1, "description": "Coffee", "amount": 50, "category": "Food", "date": "2026-09-10"},
    {"id": 3, "description": "Taxi", "amount": 100, "category": "Transport", "date": "2026-09-10"}]
        with patch("expenses_tracker.save_expenses"):
            add_expense(expenses, "Doughnuts", 205, "Food", "2026-09-10")
        self.assertEqual(len(expenses), 3)
        self.assertEqual(expenses[2]["id"], 4)

class TestUpdateExpense(unittest.TestCase):
    def setUp(self):
        self.expenses = [{
        "id": 1, "description": "Pancakes", "amount": 50,
        "category": "Food",
        "date": "2026-09-10"}]

    def test_valid_id_and_one_field(self):
        expenses = self.expenses
        with patch("expenses_tracker.save_expenses"):
            update_expense(expenses, 1, amount=200)
        self.assertEqual(expenses[0]["amount"], 200)
    
    def test_valid_id_and_more_than_one_fields(self):
        expenses = self.expenses

        with patch("expenses_tracker.save_expenses"):
            update_expense(expenses, 1, amount=200, category="Dessert",
                           date="2026-09-11",description="Chocolate Pancakes")
        self.assertEqual(expenses[0]["amount"], 200)
        self.assertEqual(expenses[0]["category"], "Dessert")
        self.assertEqual(expenses[0]["date"], "2026-09-11")
        self.assertEqual(expenses[0]["description"], "Chocolate Pancakes")

    def test_invalid_id(self):
        expenses = self.expenses

        with patch("expenses_tracker.save_expenses"):
            update_expense(expenses, 2, amount=200)
        self.assertEqual(expenses[0]["amount"], 50)
    
    def test_no_fields_provided(self):
        expenses = self.expenses

        with patch("expenses_tracker.save_expenses"):
            update_expense(expenses, 1)
        self.assertEqual(expenses[0]['description'], "Pancakes")
        self.assertEqual(expenses[0]['amount'], 50)
        self.assertEqual(expenses[0]['category'], "Food")
        self.assertEqual(expenses[0]['date'], "2026-09-10")

    def test_unchanged_fields(self):
        expenses = self.expenses

        with patch("expenses_tracker.save_expenses"):
            update_expense(expenses, 1, amount=100)
        self.assertEqual(expenses[0]['description'], "Pancakes")
        self.assertEqual(expenses[0]['amount'], 100)
        self.assertEqual(expenses[0]['category'], "Food")
        self.assertEqual(expenses[0]['date'], "2026-09-10")

class TestDeleteExpense(unittest.TestCase):
    def setUp(self):
        self.expenses = [{
        "id": 1, "description": "Pancakes", "amount": 50,
        "category": "Food",
        "date": "2026-09-10"}]

    def test_delete_existing_id(self):
        expenses = self.expenses
        with patch("expenses_tracker.save_expenses"):
            delete_expense(expenses, 1)
        self.assertEqual(expenses, [])

    def test_delete_nonexistent_id(self):
        expenses = self.expenses
        expected = self.expenses.copy()
        with patch("expenses_tracker.save_expenses"):
            delete_expense(expenses, 2)
        self.assertEqual(expenses, expected)

    def test_delete_empty_list(self):
        expenses = []
        with patch("expenses_tracker.save_expenses"):
            delete_expense(expenses, 1)
        self.assertEqual(expenses, [])

class TestMonthlyTotal(unittest.TestCase):

    def test_correct_month_totaled(self):
        current_year = datetime.now().year
        expenses = [{
        "id": 1, "description": "Pancakes", "amount": 50,
        "category": "Food",
        "date": f"{current_year}-09-10"}, {
        "id": 2, "description": "Cookies", "amount": 60,
        "category": "Food",
        "date": f"{current_year}-09-11"}]

        total = get_monthly_total(expenses, 9)
        self.assertEqual(total, 110)

    def test_ignore_other_months(self):
        current_year = datetime.now().year
        expenses = [{
        "id": 1, "description": "Pancakes", "amount": 50,
        "category": "Food",
        "date": f"{current_year}-09-10"}, {
        "id": 2, "description": "Cookies", "amount": 60,
        "category": "Food",
        "date": f"{current_year}-08-11"}]

        total = get_monthly_total(expenses, 9)
        self.assertEqual(total, 50)

    def test_ignore_other_years(self):

        current_year = datetime.now().year
        expenses = [{
        "id": 1, "description": "Pancakes", "amount": 50,
        "category": "Food",
        "date": f"{current_year}-09-10"}, {
        "id": 2, "description": "Cookies", "amount": 60,
        "category": "Food",
        "date": f"{current_year - 1}-09-11"}]

        total = get_monthly_total(expenses, 9)
        self.assertEqual(total, 50)

class TestShowSummary(unittest.TestCase):
    def test_correct_amounts(self):
        expenses = [{
        "id": 1, "description": "Pancakes", "amount": 50,
        "category": "Food",
        "date": "2026-09-10"}, {
        "id": 2, "description": "Cookies", "amount": 60,
        "category": "Food",
        "date": "2026-10-11"}]
        output = StringIO()
        with redirect_stdout(output):
            show_summary(expenses)
        result = output.getvalue()
        self.assertIn("110.00", result)

    def test_empty_list(self):
        expenses = []
        output = StringIO()
        with redirect_stdout(output):
            show_summary(expenses)
        result = output.getvalue()
        self.assertEqual(result.strip(), "No expenses found.")

class TestFilterByCategory(unittest.TestCase):
    def setUp(self):
        self.expenses = [{
        "id": 1, "description": "Pancakes", "amount": 50,
        "category": "Food",
        "date": "2026-09-10"}, {
        "id": 2, "description": "Cookies", "amount": 60,
        "category": "food",
        "date": "2026-10-11"}, {
        "id": 3, "description": "Burger", "amount": 100,
        "category": "Food",
        "date": "2026-10-12"}, {
        "id": 4, "description": "T-shirt", "amount": 200,
        "category": "Clothes",
        "date": "2026-10-15"}]

    def test_match_categories_case_insensitive(self):
        expenses = self.expenses
        output = StringIO()
        with redirect_stdout(output):
            filter_by_category(expenses, category="food")
        result = output.getvalue()
        self.assertIn("Pancakes", result)
        self.assertIn("Burger", result)
    def test_no_matching_categories(self):
        expenses = self.expenses
        output = StringIO()
        with redirect_stdout(output):
            filter_by_category(expenses, category="notfood")
        result = output.getvalue()
        self.assertIn("No expenses found under this category.", result)

class TestSetBudget(unittest.TestCase):
    def test_set_new_budget(self):
        budgets = {}
        current_year = datetime.now().year
        key = f"{current_year}-09"
        with patch("expenses_tracker.save_budgets"):
            set_budget(budgets, 9, 1300)
        self.assertEqual(budgets[key], 1300)

    def test_resetting_same_month_budget(self):
        current_year = datetime.now().year
        budgets = {
            f"{current_year}-09": 1500
        }
        key = f"{current_year}-09"
        with patch("expenses_tracker.save_budgets"):
            set_budget(budgets, month=9, amount=1200)
        self.assertEqual(budgets[key],1200)

    def test_invalid_month(self):
        budgets = {}
        with patch("expenses_tracker.save_budgets"):
            with self.assertRaises(ValueError):
                set_budget(budgets, 13, 1500)
    def test_invalid_amount(self):
        budgets = {}
        with patch("expenses_tracker.save_budgets"):
            with self.assertRaises(ValueError):
                set_budget(budgets, 12, -1500)

class TestCheckBudget(unittest.TestCase):
    def test_under_budget(self):
        current_year = datetime.now().year
        budgets = {f"{current_year}-09": 150}
        expenses = [{
        "id": 1, "description": "Pancakes", "amount": 50,
        "category": "Food",
        "date": f"{current_year}-09-10"},{
        "id": 2, "description": "Waffles", "amount": 50,
        "category": "Food",
        "date": f"{current_year}-09-11"},]
        output = StringIO()
        with redirect_stdout(output):
            check_budget(expenses, budgets, month=9)
        result = output.getvalue()
        self.assertIn("Remaining of the budget: 50.00", result)

    def test_over_budget(self):
        current_year = datetime.now().year
        budgets = {f"{current_year}-09": 200}
        expenses = [{
        "id": 1, "description": "Pancakes", "amount": 110,
        "category": "Food",
        "date": f"{current_year}-09-10"},{
        "id": 2, "description": "Waffles", "amount": 100,
        "category": "Food",
        "date": f"{current_year}-09-11"},]
        output = StringIO()
        with redirect_stdout(output):
            check_budget(expenses, budgets, month=9)
        result = output.getvalue()
        self.assertIn("Warning: Monthly budget exceeded by 10.00", result)

    def test_no_budget_set(self):
        current_year = datetime.now().year
        budgets = {}
        expenses = [{
        "id": 1, "description": "Pancakes", "amount": 110,
        "category": "Food",
        "date": f"{current_year}-09-10"},{
        "id": 2, "description": "Waffles", "amount": 100,
        "category": "Food",
        "date": f"{current_year}-09-11"},]
        output = StringIO()
        with redirect_stdout(output):
            check_budget(expenses, budgets, month=9)
        result = output.getvalue()
        self.assertIn("No budget was set for that month.", result)

if __name__ == "__main__":
    unittest.main()