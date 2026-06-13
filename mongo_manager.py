# mongo_manager.py

import certifi
from pymongo import MongoClient
from expense import Expense

class MongoDataManager:
    def __init__(self, uri):
        self.client = MongoClient(uri, tlsCAFile=certifi.where())
        self.db = self.client["expense_db"]
        self.collection = self.db["expenses"]
        self.expenses = self.load_expenses()

    def load_expenses(self):
        # Fetch from MongoDB and convert back to Expense objects
        data = list(self.collection.find({}, {"_id": 0}))
        return [Expense.from_dict(item) for item in data]

    def save_expenses(self):
        # MongoDB handles 'saving' individual items, 
        # but if you need a full save, you could clear/insert.
        # For a tracker, we usually just add/delete individually.
        pass

    def add_expense(self, expense):
        self.collection.insert_one(expense.to_dict())
        self.expenses = self.load_expenses()

    def delete_expense(self, index):
        # We find the specific item by index to delete it
        expense_to_delete = self.expenses[index]
        self.collection.delete_one({"category": expense_to_delete.category, 
                                    "amount": expense_to_delete.amount, 
                                    "date": expense_to_delete.to_dict()["date"]})
        self.expenses = self.load_expenses()