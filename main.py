from fastapi import FastAPI
from pydantic import BaseModel
from manager_factory import get_manager # Ensure this works with your env vars

app = FastAPI()
db = get_manager()

# Pydantic model for receiving data from web requests
class ExpenseSchema(BaseModel):
    category: str
    amount: float

@app.get("/")
def read_root():
    return {"message": "Expense Tracker API is running"}

@app.get("/expenses")
def get_expenses():
    # Return your data as a list of dictionaries
    return [e.__dict__ for e in db.expenses]

@app.post("/expenses")
def add_expense(expense: ExpenseSchema):
    from expense import Expense
    import datetime
    
    new_expense = Expense(datetime.date.today(), expense.category, expense.amount)
    db.add_expense(new_expense)
    return {"status": "success", "data": new_expense.__dict__}