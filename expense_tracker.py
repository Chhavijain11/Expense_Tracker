import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# File to store expenses
DATA_FILE = 'expenses.json'

class ExpenseTracker:
    def __init__(self):
        self.expenses: List[Dict] = []
        self.load_data()

    def load_data(self):
        """Load expenses from JSON file."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    self.expenses = json.load(f)
                print(f"Loaded {len(self.expenses)} expenses from {DATA_FILE}.")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading data: {e}. Starting with empty list.")
                self.expenses = []
        else:
            self.expenses = []

    def save_data(self):
        """Save expenses to JSON file."""
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(self.expenses, f, indent=4)
            print(f"Saved {len(self.expenses)} expenses to {DATA_FILE}.")
        except IOError as e:
            print(f"Error saving data: {e}")

    def validate_amount(self, amount: str) -> Optional[float]:
        """Validate and parse amount (must be positive float)."""
        try:
            amt = float(amount)
            if amt <= 0:
                print("Error: Amount must be positive.")
                return None
            return amt
        except ValueError:
            print("Error: Amount must be a valid number.")
            return None

    def validate_date(self, date_str: str) -> Optional[str]:
        """Validate date format (YYYY-MM-DD)."""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            print("Error: Date must be in YYYY-MM-DD format.")
            return None

    def add_expense(self, amount: str, date: str, note: str, category: str = "Uncategorized"):
        """Add a new expense."""
        validated_amount = self.validate_amount(amount)
        validated_date = self.validate_date(date)
        if validated_amount is None or validated_date is None:
            return False

        expense = {
            'amount': validated_amount,
            'date': validated_date,
            'note': note.strip(),
            'category': category.strip() or "Uncategorized"
        }
        self.expenses.append(expense)
        self.save_data()
        print("Expense added successfully.")
        return True

    def view_expenses(self, filter_category: Optional[str] = None, filter_date: Optional[str] = None):
        """View all or filtered expenses."""
        if not self.expenses:
            print("No expenses found.")
            return

        filtered = self.expenses
        if filter_category:
            filtered = [e for e in filtered if e['category'].lower() == filter_category.lower()]
        if filter_date:
            filtered = [e for e in filtered if e['date'] == filter_date]

        if not filtered:
            print("No expenses match the filter.")
            return

        print("\nExpenses:")
        for i, exp in enumerate(filtered, 1):
            print(f"{i}. Date: {exp['date']}, Amount: ${exp['amount']:.2f}, Category: {exp['category']}, Note: {exp['note']}")

    def update_expense(self, index: int, amount: Optional[str] = None, date: Optional[str] = None,
                       note: Optional[str] = None, category: Optional[str] = None):
        """Update an expense by index (1-based)."""
        if not (1 <= index <= len(self.expenses)):
            print("Error: Invalid expense index.")
            return False

        exp = self.expenses[index - 1]
        if amount:
            validated = self.validate_amount(amount)
            if validated is not None:
                exp['amount'] = validated
        if date:
            validated = self.validate_date(date)
            if validated is not None:
                exp['date'] = validated
        if note is not None:
            exp['note'] = note.strip()
        if category is not None:
            exp['category'] = category.strip() or "Uncategorized"

        self.save_data()
        print("Expense updated successfully.")
        return True

    def delete_expense(self, index: int):
        """Delete an expense by index (1-based)."""
        if not (1 <= index <= len(self.expenses)):
            print("Error: Invalid expense index.")
            return False

        deleted = self.expenses.pop(index - 1)
        print(f"Deleted expense: {deleted['date']} - ${deleted['amount']:.2f} ({deleted['category']})")
        self.save_data()
        return True

    def show_summary(self):
        """Show summary: total spent, by category, by month."""
        if not self.expenses:
            print("No expenses for summary.")
            return

        total = sum(e['amount'] for e in self.expenses)
        print(f"\nTotal spent: ${total:.2f}")

        # Group by category
        by_category = {}
        for e in self.expenses:
            cat = e['category']
            by_category[cat] = by_category.get(cat, 0) + e['amount']
        print("\nBy Category:")
        for cat, amt in sorted(by_category.items()):
            print(f"  {cat}: ${amt:.2f}")

        # Group by month (extract YYYY-MM from date)
        by_month = {}
        for e in self.expenses:
            month = e['date'][:7]  # YYYY-MM
            by_month[month] = by_month.get(month, 0) + e['amount']
        print("\nBy Month:")
        for month, amt in sorted(by_month.items()):
            print(f"  {month}: ${amt:.2f}")

def main():
    tracker = ExpenseTracker()
    print("Personal Expense Tracker CLI")
    print("Commands: add, view, update, delete, summary, filter [category/date], quit")

    while True:
        cmd = input("\nEnter command: ").strip().lower()
        if cmd == 'quit':
            break
        elif cmd == 'add':
            amount = input("Amount: ")
            date = input("Date (YYYY-MM-DD): ")
            note = input("Note: ")
            category = input("Category (optional): ")
            tracker.add_expense(amount, date, note, category)
        elif cmd == 'view':
            tracker.view_expenses()
        elif cmd == 'summary':
            tracker.show_summary()
        elif cmd == 'filter':
            filter_type = input("Filter by (category/date): ").strip().lower()
            if filter_type == 'category':
                cat = input("Category: ")
                tracker.view_expenses(filter_category=cat)
            elif filter_type == 'date':
                date = input("Date (YYYY-MM-DD): ")
                tracker.view_expenses(filter_date=date)
            else:
                print("Invalid filter type.")
        elif cmd == 'update':
            try:
                index = int(input("Expense index (1-based): "))
                print("Leave blank to skip: amount, date, note, category")
                amount = input("New amount: ") or None
                date = input("New date (YYYY-MM-DD): ") or None
                note = input("New note: ") or None
                category = input("New category: ") or None
                tracker.update_expense(index, amount, date, note, category)
            except ValueError:
                print("Error: Index must be a number.")
        elif cmd == 'delete':
            try:
                index = int(input("Expense index (1-based): "))
                tracker.delete_expense(index)
            except ValueError:
                print("Error: Index must be a number.")
        else:
            print("Unknown command. Try: add, view, update, delete, summary, filter, quit")

if __name__ == "__main__":
    main()