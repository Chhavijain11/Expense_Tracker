# Personal Expense Tracker

A simple CLI-based personal expense tracker built in Python. Track your expenses with categories, view summaries, and persist data to a JSON file.

## Features

### Must-Have
- **Add Expense**: Add amount (positive number), date (YYYY-MM-DD), note, and optional category.
- **View Expenses**: List all expenses (with indexing for updates/deletes).
- **Update Expense**: Modify amount, date, note, or category by index.
- **Delete Expense**: Remove by index.
- **Data Persistence**: Saves/loads from `expenses.json` (automatic on add/update/delete).
- **Validation & Error Handling**: Checks for positive amounts, valid dates, valid indices; handles file I/O errors gracefully.

### Good-to-Have
- **Categories**: Optional (defaults to "Uncategorized"); used in adds/updates.
- **Summary Reports**: Total spent, grouped by category, grouped by month (YYYY-MM).
- **Filters**: View by category or exact date.
- **CLI Interface**: Interactive menu-driven prompts.

## How to Run

1. Ensure Python 3.x is installed (no external libraries needed).
2. Save the code as `expense_tracker.py`.
3. Run: `python expense_tracker.py`
4. Follow the prompts:
   - `add`: Interactive input for new expense.
   - `view`: Shows all expenses.
   - `update`: Select index, then optional fields to change.
   - `delete`: Select index to remove.
   - `summary`: Displays totals and groupings.
   - `filter`: Choose category or date to filter views.
   - `quit`: Exit.

Data is stored in `expenses.json` in the same directory. It auto-loads on start and saves on changes.
