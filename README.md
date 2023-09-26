# FinLit
## 1. Introduction
This manual provides a comprehensive guide to using and understanding FinLit, a Python-based financial tracking tool. FinLit was created with the intention to improve the financial literacy of people. FinLit is a work in progress so far, with the encryption and decryption processes still being refined, and new features such as user authentication, categories and tags, visualizations, and more coming soon.
## 2. Installation
Before you can use FinLit, you will need to install Python 3.x. Here are the steps to get started:
1. Clone this repository to your computer: git clone https://github.com/phcj03/FinLit.git
2. Install the required Python packages: pip install -r requirements.txt
## 3. Getting Started
To launch FinLit, run this command in your terminal: python finlit.py
This command will start the application, and you will be presented with the main menu.
## 4. Features
### 1. Creating Accounts
To create a new financial account, select option "1" from the main menu.
You will be prompted to enter the account name, type, and number.
Existing account names are checked to avoid duplication.
### 2. Adding Income
To record income, select option "2" from the main menu.
Enter the account name, income amount, and a description.
### 3. Adding Expenses
To record expenses, select option "3" from the main menu.
Enter the account name, expense amount, and a description.
The application checks if expenses exceed your set budget.
### 4. Viewing Account Balance
To view the balance of an account, select option "4" and enter the account name.
### 5. Viewing Transaction History
To see transaction history for an account, choose option "5" and enter the account name.
### 6. Searching Transactions
To search for specific transactions, choose option "6" and enter the account name and a keyword.
### 7. Filtering Transactions
To filter transactions by type (e.g., Income or Expense), select option "7" and provide the account name and criteria.
### 8. Setting a Budget
Set your budget by choosing option "8" from the main menu.
Enter the desired budget amount.
### 9. Sending Notifications
To send notifications for account-related events, select option "9."
### 10. Predicting Future Expenses
Predict future expenses using linear regression by selecting option "10" and providing the account name.
### 11. Importing Data
To import data from a file, choose option "11" and enter the account name and file path.
### 12. Exporting Data
Export account data to a CSV file by selecting option "12" and specifying the account name and file path.
### 13. Backing Up Data
To create a data backup in JSON format, select option "13" and provide the account name and file path.
### 14. Restoring Data
Restore data from a JSON backup file by choosing option "14" and entering the account name and file path.
## 5. Security
FinLit uses Fernet encryption to protect sensitive data like account names and numbers.
Ensure the encryption key is stored securely, and consider additional security measures if required.
## 6. Contributing
If you'd like to contribute to FinLit, please email me at ph2265@nyu.edu.
Contributions and bug reports are welcome.
## 7. License
FinLit is licensed under the MIT License.
Review the license for more details on usage and distribution.
