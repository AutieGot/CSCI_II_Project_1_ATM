class Account:
    def __init__(self, name: str, balance: float = 0):
        """
        Sets the default values for account object.

        :param name: The name of the account.
        :param balance: The monetary value that the account holds.
        """
        self.__account_name = name
        self.__account_balance = round(balance, 2)
        self.set_balance(self.__account_balance)

    def deposit(self, amount: float) -> bool:
        """
        Increase the account balance by the specified amount.

        :param amount: The monetary value that the account balance is increasing by.
        :return: Boolean value True if the deposit transaction is successful and False if the transaction is unsuccessful.
        """
        amount = round(amount, 2)
        if amount > 0:
            self.__account_balance += amount
            return True
        return False

    def withdraw(self, amount: float) -> bool:
        """
        Decrease the account balance by the specified amount.

        :param amount: The monetary value that the account balance is decreasing by.
        :return: Boolean value True if the withdrawal transaction is successful and False if the transaction is unsuccessful.
        """
        amount = round(amount, 2)
        if 0 < amount <= self.__account_balance:
            self.__account_balance -= amount
            return True
        return False

    def get_balance(self) -> float:
        """
        Return the account balance.

        :return: Account balance.
        """
        return self.__account_balance

    def get_name(self) -> str:
        """
        Return the account name.

        :return: Account name.
        """
        return self.__account_name

    def set_balance(self, value: float):
        """
        Set the account balance to the value provided.

        :param value: Balance that the account balance is being set equal to.
        """
        value = round(value, 2)
        if value > 0:
            self.__account_balance = value
        else:
            self.__account_balance = 0

    def set_name(self, value: float):
        """
        Set the account name to the value provided.

        :param value: Name that the account name is being set equal to.
        """
        self.__account_name = value

    def __str__(self) -> str:
        """
        Return the account details.

        :return: Account name and account balance.
        """
        return f'Checking_Balance {self.get_balance()}'

class SavingAccount(Account):
    MINIMUM = 100
    RATE = 0.02

    def __init__(self, name: str, balance: float = MINIMUM):
        """
        Set the default values for each saving account object.

        :param name: The name of the saving account.
        """
        super().__init__(name, round(balance))
        self.__deposit_count = 0

    def apply_interest(self):
        """
        This should apply a 2% interest rate to the saving account balance for every 5 deposits made on the saving account.
        """
        super().set_balance(round(self.get_balance() * (1 + SavingAccount.RATE), 2))

    def deposit(self, amount: float) -> bool:
        """
        Increase the saving account balance by the specified amount and possibly apply interest based on the number of deposits made.

        :param amount: The monetary value that the saving account balance is increasing by.
        :return: Boolean value True if the deposit transaction is successful and False if the transaction is unsuccessful.
        """
        amount = round(amount, 2)
        if super().deposit(amount):
            self.__deposit_count += 1
            if self.__deposit_count % 5 == 0:
                self.apply_interest()
            return True
        return False

    def withdraw(self, amount: float) -> bool:
        """
        Decrease the saving account balance by the specified amount.

        :param amount: The monetary value that the saving account balance is decreasing by.
        :return: Boolean value True if the withdrawal transaction is successful and False if the transaction is unsuccessful.
        """
        amount = round(amount, 2)
        if 0 < amount <= super().get_balance() - SavingAccount.MINIMUM:
            super().set_balance(super().get_balance() - amount)
            return True
        return False

    def set_balance(self, value: float):
        """
        Set the saving account balance to the value provided.

        :param value: Balance that the account balance is being set equal to.
        """
        value = round(value, 2)
        if value > SavingAccount.MINIMUM:
            super().set_balance(value)
        else:
            super().set_balance(SavingAccount.MINIMUM)

    def __str__(self) -> str:
        """
        Return the account details.

        :return: Saving account name and account balance.
        """
        return f'Savings_Balance {self.get_balance()}'