# data_manager.py

import json
from expense import Expense

class DataManager:
    
    def __init__(self, filename):
        self.filename = filename
        self.expenses = self.load_expenses() or []

    def load_expenses(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                return [Expense.from_dict(expense) for expense in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_expenses(self):
        data = [expense.to_dict() for expense in self.expenses]
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def add_expense(self, expense):
        self.expenses.append(expense)
        self.save_expenses()

    def delete_expense(self, index):
        if index < len(self.expenses):
            del self.expenses[index]
            self.save_expenses()