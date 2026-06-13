from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from manager_factory import get_data_manager

app = FastAPI()
db = get_data_manager()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    # Pass 'request' as an argument, then the template name, 
    # then the context dictionary
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"expenses": db.expenses}
    )

@app.post("/add")
def add_expense(category: str, amount: float):
    from expense import Expense
    import datetime
    db.add_expense(Expense(datetime.date.today(), category, amount))
    return {"status": "success"}

@app.post("/delete/{index}")
def delete_expense(index: int):
    db.delete_expense(index)
    return {"status": "deleted"}