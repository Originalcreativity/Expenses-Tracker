import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

EXPENSE_FILE = "expenses.json"

def load_expenses():
    if not os.path.exists(EXPENSE_FILE):
        return {}
    
    with open(EXPENSE_FILE, 'r') as file:
        return json.load(file)

def save_expenses(expenses):
    with open(EXPENSE_FILE, 'w') as file:
        json.dump(expenses, file, indent=4)

class ExpenseTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expenses Tracker")
        self.geometry("700x600")  # Increased size for better visibility
        self.configure(bg="#2E2E2E")  # Dark background for contrast
        self.user = None
        self.expenses = load_expenses()

        self.create_styles()
        self.create_widgets()

    def create_styles(self):
        style = ttk.Style()
        style.configure('TButton', background='red', foreground='black', font=('Arial', 16), padding=15)
        style.map('TButton', background=[('active', '#FF4D4D')])  # Lighter red on hover
        style.configure('TLabel', background="#2E2E2E", foreground="white", font=('Arial', 16))
        style.configure('TEntry', font=('Arial', 16), padding=10)
        style.configure('TFrame', background="#2E2E2E")

    def create_widgets(self):
        self.login_frame = ttk.Frame(self)
        self.login_frame.pack(pady=40)

        self.lbl_username = ttk.Label(self.login_frame, text="Username:")
        self.lbl_username.grid(row=0, column=0, padx=10, pady=10)

        self.ent_username = ttk.Entry(self.login_frame, width=40)
        self.ent_username.grid(row=0, column=1, padx=10, pady=10)

        self.btn_login = ttk.Button(self.login_frame, text="Login", command=self.login)
        self.btn_login.grid(row=1, column=0, columnspan=2, pady=10)

        self.btn_create_account = ttk.Button(self.login_frame, text="Create Account", command=self.create_account)
        self.btn_create_account.grid(row=2, column=0, columnspan=2, pady=10)

        self.expense_frame = None

    def login(self):
        username = self.ent_username.get().strip()
        if username:
            self.user = username
            self.login_frame.pack_forget()
            self.show_expense_frame()
        else:
            messagebox.showwarning("Warning", "Please enter a username.")

    def create_account(self):
        username = simpledialog.askstring("Create Account", "Enter a new username:")
        if username:
            if username in self.expenses:
                messagebox.showwarning("Warning", "Username already exists. Try another.")
            else:
                self.expenses[username] = []
                save_expenses(self.expenses)
                messagebox.showinfo("Success", "Account created successfully!")

    def show_expense_frame(self):
        self.expense_frame = ttk.Frame(self)
        self.expense_frame.pack(pady=20)

        self.lbl_title = ttk.Label(self.expense_frame, text=f"Welcome, {self.user}!", font=('Arial', 24))
        self.lbl_title.pack(pady=10)

        self.btn_add_expense = ttk.Button(self.expense_frame, text="Add Expense", command=self.add_expense)
        self.btn_add_expense.pack(pady=10, fill=tk.X)

        self.btn_view_expenses = ttk.Button(self.expense_frame, text="View Expenses", command=self.view_expenses)
        self.btn_view_expenses.pack(pady=10, fill=tk.X)

        self.btn_delete_expense = ttk.Button(self.expense_frame, text="Delete Expense", command=self.delete_expense)
        self.btn_delete_expense.pack(pady=10, fill=tk.X)

        self.btn_logout = ttk.Button(self.expense_frame, text="Logout", command=self.logout)
        self.btn_logout.pack(pady=10, fill=tk.X)

    def add_expense(self):
        description = simpledialog.askstring("Add Expense", "Enter description:")
        amount = simpledialog.askfloat("Add Expense", "Enter amount:")
        category = simpledialog.askstring("Add Expense", "Enter category:")
        date = simpledialog.askstring("Add Expense", "Enter date (YYYY-MM-DD):")
        
        if description and amount and category and date:
            expense = {
                'description': description,
                'amount': amount,
                'category': category,
                'date': date
            }
            self.expenses[self.user].append(expense)
            save_expenses(self.expenses)
            messagebox.showinfo("Success", "Expense added successfully!")

            # Ask if the user wants to add another expense
            self.ask_add_another()

    def ask_add_another(self):
        response = messagebox.askyesno("Add Another Expense", "Do you want to add another expense?")
        if response:
            self.add_expense()  # Call the method again for new input

    def view_expenses(self):
        if self.user in self.expenses and self.expenses[self.user]:
            expenses_list = "\n".join(
                [f"{i}. {exp['description']} - ${exp['amount']} ({exp['category']}) on {exp.get('date', 'No date provided')}" 
                 for i, exp in enumerate(self.expenses[self.user])]
            )
            messagebox.showinfo("Your Expenses", expenses_list)
        else:
            messagebox.showinfo("Your Expenses", "No expenses recorded.")

    def delete_expense(self):
        index = simpledialog.askinteger("Delete Expense", "Enter index of expense to delete:")
        if index is not None and self.user in self.expenses and 0 <= index < len(self.expenses[self.user]):
            del self.expenses[self.user][index]
            save_expenses(self.expenses)
            messagebox.showinfo("Success", "Expense deleted successfully!")
        else:
            messagebox.showwarning("Warning", "Invalid index.")

    def logout(self):
        self.user = None
        self.expense_frame.pack_forget()
        self.login_frame.pack(pady=40)

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()
