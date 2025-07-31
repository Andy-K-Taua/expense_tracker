# expense.py

import datetime

class Expense:

    def __init__(self, date, category, amount):
        self.date = date
        self.category = category
        self.amount = amount

    def to_dict(self):
        if isinstance(self.date, str):
            date = self.date
        else:
            date = self.date.strftime("%d-%m-%Y")
        return {
            "date": date,
            "category": self.category,
            "amount": self.amount
        }

    @classmethod
    def from_dict(cls, data):
        date_formats = ["%d-%m-%Y"]
        for date_format in date_formats:
            try:
                date = datetime.datetime.strptime(data["date"], date_format).date()
                return cls(date, data["category"], data["amount"])
            except ValueError:
                pass
        raise ValueError(f"Invalid date format: {data['date']}. Expected DD-MM-YYYY.")