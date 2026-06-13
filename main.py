from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from manager_factory import get_data_manager

app = FastAPI()
db = get_data_manager()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    # Pass the list of expenses directly to the HTML template
    return templates.TemplateResponse("index.html", {"request": request, "expenses": db.expenses})

@app.post("/add")
def add_expense(category: str, amount: float):
    from expense import Expense
    import datetime
    db.add_expense(Expense(datetime.date.today(), category, amount))
    return {"status": "success"}