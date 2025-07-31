import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import datetime 
from expense import Expense
from data_manager import DataManager

class ExpenseTracker(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("My Expense Tracker")

        self.geometry("800x800")

        self.data_manager = DataManager("expenses.json")
        self.expenses = getattr(self.data_manager, 'expenses', [])

        # Create tab view

        open_button = ctk.CTkButton(self, text="Open New Window", command=lambda: [new_window := ctk.CTkToplevel(self), new_window.title("New Window"), new_window.geometry("900x700")])
        open_button.pack(pady=10)

        self.tab_view = ctk.CTkTabview(self, width=900, height=700)
        self.tab_view.pack(pady=20)

        self.tab_view.add("Expenses")
        self.tab_view.add("File")

        

        # Expenses tab

        self.expenses_tab = self.tab_view.tab("Expenses")

        self.expense_label = ctk.CTkLabel(self.expenses_tab, text="Expense Category:")
        self.expense_label.pack(pady=(50, 5))  
        self.expense_entry = ctk.CTkEntry(self.expenses_tab, width=250)
        self.expense_entry.pack()

        self.amount_label = ctk.CTkLabel(self.expenses_tab, text="Amount:")
        self.amount_label.pack(pady=(20, 5))
        self.amount_entry = ctk.CTkEntry(self.expenses_tab, width=250)
        self.amount_entry.pack()

        self.date_label = ctk.CTkLabel(self.expenses_tab, text="Date (DD-MM-YYYY):")
        self.date_label.pack(pady=(20, 5))
        self.date_entry = ctk.CTkEntry(self.expenses_tab, width=250)
        self.date_entry.pack()

        self.use_current_date_button = ctk.CTkButton(self.expenses_tab, text="Use Current Date", command=self.use_current_date)
        self.use_current_date_button.pack(pady=30)

        self.add_button = ctk.CTkButton(self.expenses_tab, text="Save Expense", command=self.add_expense)
        self.add_button.pack(pady=10)

        self.expenses_frame = ctk.CTkScrollableFrame(self.expenses_tab, width=600, height=250)
        self.expenses_frame.pack()

        self.update_expenses_frame()

        open_button = ctk.CTkButton(self, text="Open New Window", command=lambda: [new_window := ctk.CTkToplevel(self), new_window.title("New Window"), new_window.geometry("300x200")])
        open_button.pack(pady=10)

        # File tab
        self.file_tab = self.tab_view.tab("File")

        self.save_button = ctk.CTkButton(self.file_tab, text="Save Expenses", command=self.save_expenses)
        self.save_button.pack(pady=20)

        self.load_button = ctk.CTkButton(self.file_tab, text="Load Expenses", command=self.load_expenses)
        self.load_button.pack(pady=20)

        self.clear_button = ctk.CTkButton(self.file_tab, text="Clear All Expenses", command=self.clear_expenses)
        self.clear_button.pack(pady=20)

        self.view_total_button = ctk.CTkButton(self.file_tab, text="View Total Expenses", command=self.view_total_expenses)
        self.view_total_button.pack(pady=20)

        self.exit_button = ctk.CTkButton(self.file_tab, text="Exit", command=self.quit)
        self.exit_button.pack(pady=20)

    def use_current_date(self):
        current_date = datetime.date.today().strftime("%d-%m-%Y")
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, current_date)

    def add_expense(self):
        category = self.expense_entry.get()
        try:
            amount = float(self.amount_entry.get())
            date = self.date_entry.get()
            if category and amount and date:
                try:
                    date_obj = datetime.datetime.strptime(date, "%d-%m-%Y").date()
                    expense = Expense(date_obj, category, amount)
                    self.data_manager.add_expense(expense)
                    self.expenses = self.data_manager.expenses
                    self.expense_entry.delete(0, "end")
                    self.amount_entry.delete(0, "end")
                    self.date_entry.delete(0, "end")
                    self.update_expenses_frame()
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format. Use DD-MM-YYYY.")
            else:
                messagebox.showerror("Error", "Please fill in all fields.")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a number.")

    def update_expenses_frame(self):
        for widget in self.expenses_frame.winfo_children():
            widget.destroy()
        for i, expense in enumerate(self.expenses):
            frame = ctk.CTkFrame(self.expenses_frame)
            frame.pack(fill="x")
            label = ctk.CTkLabel(frame, text=f"{i+1}. {expense.category} - ${expense.amount:.2f} on {expense.date.strftime('%d-%m-%Y')}")
            label.pack(side="left")
            button = ctk.CTkButton(frame, text="Delete", command=lambda i=i: self.delete_expense(i))
            button.pack(side="right", pady=(4))

    def delete_expense(self, index):
        self.data_manager.delete_expense(index)
        self.expenses = self.data_manager.expenses
        self.update_expenses_frame()

    def save_expenses(self):
        self.data_manager.save_expenses()

    def load_expenses(self):
        self.expenses = self.data_manager.load_expenses()
        self.update_expenses_frame()

    def clear_expenses(self):
        self.data_manager.expenses = []
        self.data_manager.save_expenses()
        self.expenses = self.data_manager.expenses
        self.update_expenses_frame()

    def view_total_expenses(self):
        total = sum(expense.amount for expense in self.expenses)
        messagebox.showinfo("Total Expenses", f"Total Expenses: ${total:.2f}")

    def open_new_window(self):
        new_window = ctk.CTkToplevel(self)
        new_window.title("New Window")
        new_window.geometry("300x200")

if __name__ == "__main__":
    app = ExpenseTracker()
    app.mainloop()