# Expense Tracker

A command-line expense tracking application built with Python.

The project allows users to record, update, delete, filter, summarize, budget, and export expenses while storing data locally in JSON files.

## Project URL

[Expense Tracker Project](https://roadmap.sh/projects/expense-tracker)

## Features

- Add a new expense with:
  - Description
  - Amount
  - Category
  - Date
- Automatically assign unique expense IDs
- Update existing expenses
- Delete expenses by ID
- View all expenses
- Filter expenses by category
- View the total amount spent
- View spending for a specific month of the current year
- Set monthly budgets
- Warn when monthly spending exceeds the budget
- Show the remaining budget when spending is below the limit
- Export expenses to a CSV file
- Validate:
  - Expense amounts
  - Budget amounts
  - Months
  - Dates
- Handle missing or invalid input
- Store expenses and budgets using JSON
- Command-line help using `argparse`
- Unit tests using Python's `unittest`

## Project Structure

```text
expense-tracker/
├── expenses_tracker.py
├── test_expenses_tracker.py
├── expenses.json
├── budgets.json
├── README.md
└── .gitignore
```

## Requirements

- Python 3.x
- No external packages are required

The project only uses Python standard-library modules such as:

- `argparse`
- `json`
- `csv`
- `datetime`
- `unittest`

## Running the Program

Open a terminal in the project folder and run:

```bash
python expenses_tracker.py
```

Running the program without a command displays the help menu.

You can also view the help menu directly:

```bash
python expenses_tracker.py --help
```

## Commands

### Add an Expense

```bash
python expenses_tracker.py add --description "Coffee" --amount 50 --category Food
```

The current date is used automatically if no date is provided.

You can also provide a date manually:

```bash
python expenses_tracker.py add --description "Lunch" --amount 120 --category Food --date 2026-09-10
```

Dates must use:

```text
YYYY-MM-DD
```

### View All Expenses

```bash
python expenses_tracker.py list
```

### Filter Expenses by Category

```bash
python expenses_tracker.py list --category Food
```

Category matching is case-insensitive.

### Update an Expense

The expense ID is required. All fields after the ID are optional.

```bash
python expenses_tracker.py update 2 --amount 200
```

You can update multiple fields at once:

```bash
python expenses_tracker.py update 2 --description "Dinner" --amount 250 --category Food --date 2026-09-11
```

### Delete an Expense

```bash
python expenses_tracker.py delete 2
```

### View Total Spending

```bash
python expenses_tracker.py summary
```

### View Spending for a Specific Month

```bash
python expenses_tracker.py summary --month 9
```

The monthly summary only includes expenses from that month in the current year.

### Set a Monthly Budget

```bash
python expenses_tracker.py budget --month 9 --amount 1500
```

After adding or updating expenses, the application checks the relevant monthly budget and reports either:

```text
Remaining of the budget: 200.00
```

or:

```text
Warning: Monthly budget exceeded by 200.00
```

### Export Expenses to CSV

```bash
python expenses_tracker.py export --filename expenses.csv
```

The generated CSV contains:

```text
id,description,amount,category,date
```

## Data Storage

Expenses are stored in:

```text
expenses.json
```

Example:

```json
[
    {
        "id": 1,
        "description": "Coffee",
        "amount": 50.0,
        "category": "Food",
        "date": "2026-09-10"
    }
]
```

Monthly budgets are stored in:

```text
budgets.json
```

Example:

```json
{
    "2026-09": 1500.0
}
```

## Validation and Error Handling

The application validates several types of user input.

Examples include:

- Expense and budget amounts must be greater than zero.
- Months must be between `1` and `12`.
- Dates must use the `YYYY-MM-DD` format.
- Invalid or nonexistent expense IDs are handled without modifying unrelated expenses.
- Updating an expense without providing any fields is detected.
- Missing category matches are reported to the user.
- Invalid JSON data is handled rather than silently overwriting corrupted data.

## Running the Tests

The project uses Python's built-in `unittest` framework.

Run the test suite with:

```bash
python test_expenses_tracker.py
```

The tests cover core functionality such as:

- Input validation
- Adding expenses
- Unique ID generation
- Updating expenses
- Deleting expenses
- Monthly totals
- Expense summaries
- Category filtering
- Monthly budgets
- Budget warnings

Some tests use `unittest.mock.patch` so that test runs do not modify the real JSON files.

## Concepts Practiced

This project was built to practice:

- Python functions
- Lists and dictionaries
- JSON file persistence
- CSV file generation
- File handling
- Loops and conditionals
- Input validation
- Exceptions with `try` / `except`
- Dates with `datetime`
- Command-line interfaces with `argparse`
- Optional and positional CLI arguments
- Reusable helper functions
- Unit testing
- Mocking file-saving functions
- Capturing printed output during tests

## Example Workflow

```bash
python expenses_tracker.py budget --month 9 --amount 1000

python expenses_tracker.py add --description "Groceries" --amount 250 --category Food

python expenses_tracker.py add --description "Taxi" --amount 80 --category Transport

python expenses_tracker.py list

python expenses_tracker.py summary --month 9

python expenses_tracker.py export --filename september_expenses.csv
```

## Future Improvements

Possible future additions include:

- Budgets by category
- Recurring expenses
- Date-range filtering
- Sorting expenses by date or amount
- Spending reports by category
- Database storage
- A graphical user interface
- Charts and visual spending analytics

## Author

Built as a Python learning project focused on file handling, command-line applications, validation, and automated testing.
