from cryptography.fernet import Fernet
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import csv
import json
class FinanceTracker:
    
    def __init__(self):
        self.accounts = {}
        self.budget = 0
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)
        self.notifications = {}

    def encrypt_data(self, data):
        try:
            encrypted_data = self.fernet.encrypt(data.encode())
            return encrypted_data
        except Exception as e:
            self.handle_error("Encryption failed", e)

    def decrypt_data(self, encrypted_data):
        try:
            decrypted_data = self.fernet.decrypt(encrypted_data).decode()
            return decrypted_data
        except Exception as e:
            self.handle_error("Decryption failed", e)

    def create_account(self):
        try:
            account_name = input("Enter account name: ")
            if not account_name:
                raise ValueError("Account name cannot be empty.")           
            if self.is_account_exists(account_name):
                print(f"Account '{account_name}' already exists.")
                return
            account_type = input("Enter account type: ")
            account_number = input("Enter account number: ")
            encrypted_name = self.encrypt_data(account_name)
            encrypted_type = self.encrypt_data(account_type)
            encrypted_number = self.encrypt_data(account_number)         
            self.accounts[encrypted_name] = {
                "type": encrypted_type,
                "number": encrypted_number,
                "balance": 0,
                "transactions": [],
            }
            print(f"Account '{account_name}' created.")
        except Exception as e:
            self.handle_error("Account creation failed", e)

    def is_account_exists(self, account_name):
        encrypted_name = self.encrypt_data(account_name)
        return encrypted_name in self.accounts

    def add_income(self):
        try:
            account_name = input("Enter account name: ")
            if not self.is_account_exists(account_name):
                print(f"Account '{account_name}' does not exist.")
                return

            amount1 = self.get_float_input("Enter the income amount: ")
            description = input("Enter a description: ")
            encrypted_name = self.encrypt_data(account_name)
            self.accounts[encrypted_name]["balance"] += amount1
            self.add_transaction(encrypted_name, "Income", amount1, description)
        except Exception as e:
            self.handle_error("Income addition failed", e)

    def add_expense(self):
        try:
            account_name = input("Enter account name: ")
            if not self.is_account_exists(account_name):
                print(f"Account '{account_name}' does not exist.")
                return
            amount2 = self.get_float_input("Enter the expense amount: ")
            description = input("Enter a description: ")
            encrypted_name = self.encrypt_data(account_name)
            total_expenses = self.calculate_total_expenses(encrypted_name)
            if total_expenses + amount2 > self.budget:
                print("Warning: Exceeded budget!")
            else:
                self.accounts[encrypted_name]["balance"] -= amount2
                self.add_transaction(encrypted_name, "Expense", amount2, description)
        except Exception as e:
            self.handle_error("Expense addition failed", e)

    def calculate_total_expenses(self, account_name):
        encrypted_name = self.encrypt_data(account_name)
        total_expenses = sum(
            [
                transaction["amount"]
                for transaction in self.accounts[encrypted_name]["transactions"]
                if transaction["type"] == "Expense"
            ]
        )
        return total_expenses

    def get_float_input(self, prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def add_transaction(self, account_name, transaction_type, amount, description):
        encrypted_name = self.encrypt_data(account_name)
        self.accounts[encrypted_name]["transactions"].append(
            {"type": transaction_type, "amount": amount, "description": description}
        )

    def view_balance(self, account_name):
        try:
            encrypted_name = self.encrypt_data(account_name)
            if encrypted_name in self.accounts:
                return self.accounts[encrypted_name]["balance"]
            else:
                print(f"Account '{account_name}' does not exist.")
        except Exception as e:
            self.handle_error("Viewing balance failed", e)

    def view_transactions(self, account_name):
        try:
            encrypted_name = self.encrypt_data(account_name)
            if encrypted_name in self.accounts:
                transactions = self.accounts[encrypted_name]["transactions"]
                print("\nTransaction History:")
                for transaction in transactions:
                    print(
                        f"{transaction['type']}: ${transaction['amount']} - {transaction['description']}"
                    )
            else:
                print(f"Account '{account_name}' does not exist.")
        except Exception as e:
            self.handle_error("Viewing transactions failed", e)

    def search_transactions(self, account_name, keyword):
        encrypted_name = self.encrypt_data(account_name)
        if encrypted_name in self.accounts:
            transactions = self.accounts[encrypted_name]["transactions"]
            matching_transactions = []
            for transaction in transactions:
                if keyword.lower() in transaction["description"].lower():
                    matching_transactions.append(transaction)
            if matching_transactions:
                print(f"Matching Transactions for account '{account_name}' with keyword '{keyword}':")
                for transaction in matching_transactions:
                    print(
                        f"{transaction['type']}: ${transaction['amount']} - {transaction['description']}"
                    )
            else:
                print(f"No matching transactions found for account '{account_name}' with keyword '{keyword}'.")
        else:
            print(f"Account '{account_name}' does not exist.")

    def filter_transactions(self, account_name, criteria):
        encrypted_name = self.encrypt_data(account_name)
        if encrypted_name in self.accounts:
            transactions = self.accounts[encrypted_name]["transactions"]
            filtered_transactions = []
            for transaction in transactions:
                if transaction["type"] == criteria:
                    filtered_transactions.append(transaction)
            if filtered_transactions:
                print(f"Filtered Transactions for account '{account_name}':")
                for transaction in filtered_transactions:
                    print(
                        f"{transaction['type']}: ${transaction['amount']} - {transaction['description']}"
                    )
            else:
                print(f"No transactions found for account '{account_name}' with criteria: {criteria}")
        else:
            print(f"Account '{account_name}' does not exist.")

    def set_budget(self):
        budget = float(input("Enter your budget: "))
        self.budget = budget

    def send_notification(self, account_name):
        encrypted_name = self.encrypt_data(account_name)
        if encrypted_name in self.accounts:
            balance = self.view_balance(encrypted_name)
            if balance < 0:
                self.notifications[encrypted_name] = f"Negative balance in account '{account_name}'."
            upcoming_bills = self.check_upcoming_bills(encrypted_name)
            if upcoming_bills:
                self.notifications[encrypted_name] = f"Upcoming bills in account '{account_name}': {', '.join(upcoming_bills)}"
            unusual_spending = self.check_unusual_spending(encrypted_name)
            if unusual_spending:
                self.notifications[encrypted_name] = f"Unusual spending in account '{account_name}': {', '.join(unusual_spending)}"
        else:
            print(f"Account '{account_name}' does not exist.")

    def check_upcoming_bills(self, account_name):
        encrypted_name = self.encrypt_data(account_name)
        transactions = self.accounts[encrypted_name]["transactions"]
        upcoming_bills = []
        for transaction in transactions:
            if "upcoming" in transaction["description"].lower():
                upcoming_bills.append(transaction["description"])
        return upcoming_bills

    def check_unusual_spending(self, account_name):
        encrypted_name = self.encrypt_data(account_name)
        transactions = self.accounts[encrypted_name]["transactions"]
        unusual_spending = []
        for transaction in transactions:
            if transaction["type"] == "Expense" and transaction["amount"] > 1000:
                unusual_spending.append(f"{transaction['description']} (${transaction['amount']:.2f})")
        return unusual_spending

    def display_notifications(self):
        if not self.notifications:
            print("No notifications.")
        else:
            for account_name, notification in self.notifications.items():
                print(notification)

    def predict_future_expenses(self):
        account_name = input("Enter account name: ")
        encrypted_name = self.encrypt_data(account_name)
        if encrypted_name in self.accounts:
            transactions = self.accounts[encrypted_name]["transactions"]
            X, y = self.prepare_data(transactions)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = LinearRegression()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            return f"Predicted RMSE of future expenses for account '{account_name}': ${rmse:.2f}"
        else:
            print(f"Account '{account_name}' does not exist.")

    def prepare_data(self, transactions):
        X = []
        y = []
        for i in range(len(transactions) - 1):
            current_transaction = transactions[i]
            next_transaction = transactions[i + 1]
            X.append([current_transaction["amount"]])
            y.append(next_transaction["amount"])
        return np.array(X), np.array(y)

    def import_data(self):
        account_name = input("Enter account name: ")
        file_path = input("Enter the file path for data import: ")
        encrypted_name = self.encrypt_data(account_name)
        if encrypted_name in self.accounts:
            try:
                with open(file_path, 'r') as file:
                    print(f"Data imported successfully for account '{account_name}'.")
            except FileNotFoundError:
                print(f"File '{file_path}' not found.")
            except Exception as e:
                print(f"An error occurred while importing data: {str(e)}")
        else:
            print(f"Account '{account_name}' does not exist.")

    def export_to_csv(self):
        account_name = input("Enter account name: ")
        file_path = input("Enter the file path for data export (CSV): ")
        encrypted_name = self.encrypt_data(account_name)
        if encrypted_name in self.accounts:
            transactions = self.accounts[encrypted_name]["transactions"]
            try:
                with open(file_path, 'w', newline='') as csvfile:
                    fieldnames = ["Type", "Amount", "Description"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for transaction in transactions:
                        writer.writerow({
                            "Type": transaction["type"],
                            "Amount": transaction["amount"],
                            "Description": transaction["description"]
                        })
                print(f"Data exported to '{file_path}' for account '{account_name}'.")
            except Exception as e:
                print(f"An error occurred while exporting data: {str(e)}")
        else:
            print(f"Account '{account_name}' does not exist.")

    def backup_data(self):
        account_name = input("Enter account name: ")
        file_path = input("Enter the file path for data backup (JSON): ")
        encrypted_name = self.encrypt_data(account_name)
        if encrypted_name in self.accounts:
            account_data = self.accounts[encrypted_name]
            try:
                with open(file_path, 'w') as file:
                    json.dump(account_data, file)
                print(f"Data backed up successfully for account '{account_name}' to '{file_path}'.")
            except Exception as e:
                print(f"An error occurred while backing up data: {str(e)}")
        else:
            print(f"Account '{account_name}' does not exist.")

    def restore_data(self):
        account_name = input("Enter account name: ")
        file_path = input("Enter the file path for data restoration (JSON): ")
        encrypted_name = self.encrypt_data(account_name)
        if encrypted_name not in self.accounts:
            try:
                with open(file_path, 'r') as file:
                    account_data = json.load(file)
                self.accounts[encrypted_name] = account_data
                print(f"Data restored successfully for account '{account_name}' from '{file_path}'.")
            except FileNotFoundError:
                print(f"File '{file_path}' not found.")
            except Exception as e:
                print(f"An error occurred while restoring data: {str(e)}")
        else:
            print(f"Account '{account_name}' already exists.")

    def handle_error(self, message, error):
        print(f"Error: {message}")
        print(f"Details: {str(error)}")

    def main_menu(self):
        print("\nFinance Tracker Menu:")
        print("1. Create Account")
        print("2. Add Income")
        print("3. Add Expense")
        print("4. View Balance")
        print("5. View Transactions")
        print("6. Search Transactions")
        print("7. Filter Transactions")
        print("8. Set Budget")
        print("9. Send Notifications")
        print("10. Predict Future Expenses")
        print("11. Import Data")
        print("12. Export Data")
        print("13. Backup Data")
        print("14. Restore Data")
        print("15. Exit")

    def start(self):
        while True:
            self.main_menu()
            choice = input("Enter your choice: ")
            if choice == "1":
                self.create_account()
            elif choice == "2":
                self.add_income()
            elif choice == "3":
                self.add_expense()
            elif choice == "4":
                account_name = input("Enter account name: ")
                balance = self.view_balance(account_name)
                if balance is not None:
                    print(f"Current Balance for '{account_name}': ${balance:.2f}")
            elif choice == "5":
                account_name = input("Enter account name: ")
                self.view_transactions(account_name)
            elif choice == "6":
                account_name = input("Enter account name: ")
                keyword = input("Enter a keyword to search transactions: ")
                self.search_transactions(account_name, keyword)
            elif choice == "7":
                account_name = input("Enter account name: ")
                criteria = input("Enter filtering criteria (e.g., Income or Expense): ")
                self.filter_transactions(account_name, criteria)
            elif choice == "8":
                self.set_budget()
            elif choice == "9":
                self.notifications = {}
                for account_name in self.accounts.keys():
                    self.send_notification(account_name)
                self.display_notifications()
                break
            elif choice == "10":
                prediction = self.predict_future_expenses()
                print(prediction)
            elif choice == "11":
                self.import_data()
            elif choice == "12":
                self.export_to_csv()
            elif choice == "13":
                self.backup_data()
            elif choice == "14":
                self.restore_data()
            elif choice == "15":
                break

if __name__ == "__main__":
    tracker = FinanceTracker()
    tracker.start()
