from accounts_gui import *
from main_logic import *
from accounts import *

class Accounts_Logic(QMainWindow, Ui_window_accounts):
    def __init__(self, id: str, first_name: str, last_name: str):
        """
        Saves user ID, first name, and last name into appropriate variables. Also defines each GUI button, the necessary label, and opens a file with the user's banking information.

        :param id: User's created ID.
        :param first_name: User's first name.
        :param last_name: User's last name.
        """
        super().__init__()
        self.setupUi(self)

        self.user_ID = id
        self.first_name = first_name
        self.last_name = last_name

        self.label_welcome.setText(f'Welcome, {self.first_name} {self.last_name}')
        self.button_logout.clicked.connect(lambda : self.logout())
        self.button_checking_deposit.clicked.connect(lambda : self.checking_deposit())
        self.button_checking_withdraw.clicked.connect(lambda : self.checking_withdraw())
        self.button_savings_deposit.clicked.connect(lambda : self.savings_deposit())
        self.button_savings_withdraw.clicked.connect(lambda : self.savings_withdraw())

        try:
            with open(f'user_files/{self.user_ID}_bank.txt', 'r') as txt_infile:
                for line in txt_infile:
                    line_list = line.split()
                    if line_list[0] == 'Checking_Balance':
                        self.user_checking = Account(f'{self.first_name}\'s Checking', float(line_list[1]))
                    elif line_list[0] == 'Savings_Balance':
                        self.user_savings = SavingAccount(f'{self.first_name}\'s Savings', float(line_list[1]))
        except FileNotFoundError:
            self.user_checking = Account(f'{self.first_name}\'s Checking')
            self.user_savings = SavingAccount(f'{self.first_name}\'s Savings')
        finally:
            self.label_checking_number.setText(f"${self.user_checking.get_balance():,.2f}")
            self.label_savings_number.setText(f"${self.user_savings.get_balance():,.2f}")

    def logout(self):
        """
        Attempts to log the save the user's data and log out the user. If it fails, the user will not be logged out.
        """
        try:
            with open(f'user_files/{self.user_ID}_bank.txt', 'w') as txt_outfile:
                txt_outfile.write(f'{self.user_checking}\n')
                txt_outfile.write(f'{self.user_savings}')
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Success!")
            dlg.setText("User was successfully logged out.")
            dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
            dlg.setIcon(QMessageBox.Icon.Information)
            dlg.exec()
            self.close()
        except FileNotFoundError:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Failure!")
            dlg.setText("User was not logged out! File could not be saved!")
            dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
            dlg.setIcon(QMessageBox.Icon.Critical)
            dlg.exec()

    def checking_deposit(self):
        """
        Deposits the amount of money from the checking account's respective input box into the user's checking account. If the user's input is invalid, a warning window will pop up.
        """
        try:
            if self.user_checking.deposit(float(self.input_checking_amount.text())):
                self.label_checking_number.setText(f'${float(self.user_checking.get_balance()):,.2f}')
            else:
                self.value_error()
        except ValueError:
            self.value_error()

    def checking_withdraw(self):
        """
        Withdraws the amount of money from the checking account's respective input box from the user's checking account. If the user's input is invalid, a warning window will pop up.
        """
        try:
            if self.user_checking.withdraw(float(self.input_checking_amount.text())):
                self.label_checking_number.setText(f'${self.user_checking.get_balance():,.2f}')
            else:
                self.value_error()
        except ValueError:
            self.value_error()

    def savings_deposit(self):
        """
        Deposits the amount of money from the saving account's respective input box into the user's savings account. If the user's input is invalid, a warning window will pop up. If the user deposits 5 times, an interest rate will be applied to the savings accout.
        """
        try:
            if self.user_savings.deposit(float(self.input_savings_amount.text())):
                self.label_savings_number.setText(f'${self.user_savings.get_balance():,.2f}')
            else:
                 self.value_error()
        except ValueError:
            self.value_error()

    def savings_withdraw(self):
        """
        Withdraws the amount of money from the saving account's respective input box from the user's savings account. If the user's input is invalid, a warning window will pop up.
        """
        try:
            if self.user_savings.withdraw(float(self.input_savings_amount.text())):
                self.label_savings_number.setText(f'${self.user_savings.get_balance():,.2f}')
            else:
                self.value_error()
        except ValueError:
            self.value_error()

    def value_error(self):
        """
        Displays a warning window that the user's input was invalid.
        """
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Error!")
        dlg.setText("Value is not valid.")
        dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
        dlg.setIcon(QMessageBox.Icon.Warning)
        dlg.exec()
        self.input_checking_amount.clear()
        self.input_savings_amount.clear()

