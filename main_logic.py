import csv
from PyQt6.QtWidgets import *
from main_gui import *

class Main_Logic(QMainWindow, Ui_window_log_sign):
    def __init__(self):
        """
        Initializes the user's ID, PIN, name, and logged in variables. Also, defines each GUI button and makes sure that the sign in labels and input boxes are not yet available.
        """
        super().__init__()
        self.setupUi(self)
        self.log()

        self.id = ''
        self.pin = ''
        self.first_name = ''
        self.last_name = ''
        self.logged_in = False

        self.button_enter.clicked.connect(lambda : self.enter())
        self.button_cancel.clicked.connect(lambda : self.cancel())
        self.radio_sign.clicked.connect(lambda : self.sign())
        self.radio_log.clicked.connect(lambda : self.log())

    def enter(self):
        """
        If the user has the log in radio button selected, this will check to make sure that the account exists, or it will display a warning window. If the user has the sign in radio button selected, this will set the user's ID, PIN, first name, and last name as long as the account does not already exist. If the input is invalid, the user can try again.
        """
        try:
            self.id = self.input_ID.text().strip()
            self.pin = self.input_PIN.text()
            if len(self.id) == 0 or len(self.pin) == 0:
                raise ValueError
            if self.radio_sign.isChecked():
                if self.check_create_user_exists():
                    dlg = QMessageBox(self)
                    dlg.setWindowTitle("Failure!")
                    dlg.setText("User already exists.")
                    dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
                    dlg.setIcon(QMessageBox.Icon.Warning)
                    dlg.exec()
                else:
                    self.first_name = self.input_first.text().strip()
                    self.last_name = self.input_last.text().strip()
                    if len(self.first_name) == 0 or len(self.last_name) == 0:
                        raise ValueError
                    with open('user_files/ATM_users.csv', 'a', newline ='') as csv_users:
                        csv_writer = csv.writer(csv_users)
                        csv_writer.writerow([self.id, self.pin, self.last_name, self.first_name])
                    dlg = QMessageBox(self)
                    dlg.setWindowTitle("Success!")
                    dlg.setText("User was successfully created.")
                    dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
                    dlg.setIcon(QMessageBox.Icon.Information)
                    dlg.exec()
                    self.logged_in = True
                    self.close()
            elif self.radio_log.isChecked():
                if self.check_existing_user_exists():
                    dlg = QMessageBox(self)
                    dlg.setWindowTitle("Success!")
                    dlg.setText("User was successfully found.")
                    dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
                    dlg.setIcon(QMessageBox.Icon.Information)
                    dlg.exec()
                    self.logged_in = True
                    self.close()
                else:
                    dlg = QMessageBox(self)
                    dlg.setWindowTitle("Failure!")
                    dlg.setText("User was not found.")
                    dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
                    dlg.setIcon(QMessageBox.Icon.Warning)
                    dlg.exec()
        except FileNotFoundError:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error!")
            dlg.setText("File not found.")
            dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
            dlg.setIcon(QMessageBox.Icon.Warning)
            dlg.exec()
        except ValueError:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error!")
            dlg.setText("Value is not valid.")
            dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
            dlg.setIcon(QMessageBox.Icon.Warning)
            dlg.exec()
        finally:
            self.input_ID.clear()
            self.input_PIN.clear()
            self.input_first.clear()
            self.input_last.clear()
            self.input_ID.setFocus()

    def log(self):
        """
        Makes the sign in labels and inputs invisible.
        """
        self.label_first.setVisible(False)
        self.label_last.setVisible(False)
        self.input_first.setVisible(False)
        self.input_last.setVisible(False)

    def sign(self):
        """
        Makes the sign in labels and inputs visible.
        """
        self.label_first.setVisible(True)
        self.label_last.setVisible(True)
        self.input_first.setVisible(True)
        self.input_last.setVisible(True)

    def cancel(self):
        """
        Creates functionality for the cancel button which closes the window without logging in.
        """
        self.close()

    def get_id(self) -> str:
        """
        Returns the user's ID.

        :return: User's ID.
        """
        return self.id

    def get_first_name(self) -> str:
        """
        Returns the user's first name.

        :return: User's first name.
        """
        return self.first_name

    def get_last_name(self) -> str:
        """
        Returns the user's last name.

        :return: User's last name.
        """
        return self.last_name

    def get_logged_in(self) -> bool:
        """
        Returns whether or not the user successfully logged or signed in to the system.

        :return: If user is logged in.
        """
        return self.logged_in

    def set_logged_in(self, log: bool):
        """
        Sets the logged in status.
        """
        self.logged_in = log

    def check_create_user_exists(self) -> bool:
        """
        Checks if a new user can be created with the given user ID.

        :return: If user ID is available.
        """
        with open('user_files/ATM_users.csv', 'r') as csv_users:
            csv_reader = csv.DictReader(csv_users)
            for line in csv_reader:
                if line['id'] == self.id:
                    self.first_name = line['first_name']
                    self.last_name = line['last_name']
                    return True
            return False

    def check_existing_user_exists(self) -> bool:
        """
        Checks if the user ID and PIN match any in the system.

        :return: If user ID and PIN match.
        """
        with open('user_files/ATM_users.csv', 'r') as csv_users:
            csv_reader = csv.DictReader(csv_users)
            for line in csv_reader:
                if line['id'] == self.id and line['pin'] == self.pin:
                    self.first_name = line['first_name']
                    self.last_name = line['last_name']
                    return True
            return False