from accounts_logic import *

def main():
    """
    Runs the main window, allowing the user to log in or sign in. If successful, a second window containing the user's bank information will appear.
    """
    application = QApplication([])
    main_window = Main_Logic()
    main_window.show()
    application.exec()
    if main_window.get_logged_in():
        accounts_window = Accounts_Logic(main_window.get_id(), main_window.get_first_name(), main_window.get_last_name())
        accounts_window.show()
        application.exec()
        main_window.set_logged_in(False)

if __name__ == '__main__':
    main()