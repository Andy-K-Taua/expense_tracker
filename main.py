import customtkinter as ctk
from tkinter import messagebox
import datetime
from data_manager import DataManager
from expense import Expense

class ExpenseTracker(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("500x700")
        
        # UI Theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Data
        self.data_manager = DataManager("expenses.json")
        self.expenses = self.data_manager.expenses

        # --- Main Container ---
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(pady=20, padx=20, fill="both", expand=True)

        # --- Header Row (Title + Total) ---
        self.header_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(self.header_frame, text="Expense Tracker", font=("Arial", 24, "bold")).pack(side="left")
        
        self.total_label = ctk.CTkLabel(self.header_frame, text="Total: $0.00", font=("Arial", 18, "bold"), text_color="#059669")
        self.total_label.pack(side="right")

        # --- Input Card ---
        self.input_card = ctk.CTkFrame(self.container, corner_radius=15, fg_color="white", border_width=1, border_color="#E5E7EB")
        self.input_card.pack(fill="x", pady=10)

        self.category_input = ctk.CTkEntry(self.input_card, placeholder_text="Category (e.g. Food)", fg_color="#F9FAFB")
        self.category_input.pack(pady=(20, 10), padx=20, fill="x")

        self.amount_input = ctk.CTkEntry(self.input_card, placeholder_text="Amount (0.00)", fg_color="#F9FAFB")
        self.amount_input.pack(pady=(0, 10), padx=20, fill="x")

        self.add_button = ctk.CTkButton(self.input_card, text="Add Expense", command=self.add_expense)
        self.add_button.pack(pady=(0, 20), padx=20, fill="x")

        # --- History Card ---
        self.history_card = ctk.CTkFrame(self.container, corner_radius=15, fg_color="white", border_width=1, border_color="#E5E7EB")
        self.history_card.pack(fill="both", expand=True, pady=10)

        ctk.CTkLabel(self.history_card, text="History", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.expenses_frame = ctk.CTkScrollableFrame(self.history_card, fg_color="transparent")
        self.expenses_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_ui()

    def refresh_ui(self):
        """Sync the list and total calculation"""
        self.update_total()
        self.update_expenses_frame()

    def update_total(self):
        total = sum(e.amount for e in self.expenses)
        self.total_label.configure(text=f"Total: ${total:.2f}")

    def add_expense(self):
        try:
            cat = self.category_input.get()
            amt = float(self.amount_input.get())
            new_expense = Expense(datetime.date.today(), cat, amt)
            self.data_manager.add_expense(new_expense)
            self.expenses = self.data_manager.expenses
            self.refresh_ui()
            self.category_input.delete(0, "end")
            self.amount_input.delete(0, "end")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")

    def delete_expense(self, index):
        self.data_manager.delete_expense(index)
        self.expenses = self.data_manager.expenses
        self.refresh_ui()

    def update_expenses_frame(self):
        for widget in self.expenses_frame.winfo_children():
            widget.destroy()
        
        if not self.expenses:
            ctk.CTkLabel(self.expenses_frame, text="No expenses yet.", text_color="gray").pack(pady=20)
            return

        for i, expense in enumerate(self.expenses):
            row = ctk.CTkFrame(self.expenses_frame, fg_color="#F9FAFB", border_width=1, border_color="#F3F4F6")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"{expense.category}", font=("Arial", 13, "bold"), padx=10).pack(side="left")
            ctk.CTkLabel(row, text=f"${expense.amount:.2f}", text_color="#059669", padx=10).pack(side="left")
            ctk.CTkButton(row, text="Delete", width=50, fg_color="transparent", text_color="red", 
                          command=lambda i=i: self.delete_expense(i)).pack(side="right", padx=5)

if __name__ == "__main__":
    app = ExpenseTracker()
    app.mainloop()