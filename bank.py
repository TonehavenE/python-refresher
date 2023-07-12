"""
Eben Quenneville

Goals:
Create a simulation of a bank account.

    The account should have a balance, a name and an account number.
    The account should have a method to withdraw money.
    The account should have a method to deposit money.
    The account should have a method to print the current balance.
"""
class BankAccount:
    """
    A representation of a bank account, with balance, name, and account number.
    """
    def __init__(self, name: str, account_number: int,  balance: int or float = 0):
        """
        Initialize an account. 
        Arguments:
            name: str, the name of the account
            account_number: the number representing the account id
            balance: the amount of money stored in the account
        """
        self.name = name
        self.balance = balance
        self.account_number = account_number

    def withdraw(self, quantity: int or float):
        """
        Withdraws <quantity: int> from the account. 
        Throws a ValueError if <quantity> is less than 0, 
        or greater than the balance of the account.
        """
        if quantity < 0:
            raise ValueError(f"{quantity} is less than 0!")
        if self.balance >= quantity:
            self.balance -= quantity
            print(f"You have successfully withdrawn {quantity} from your account.")
        else:
            raise ValueError(f"You don't have enough money in your account to withdraw {quantity}!")
    
    def deposit(self, quantity: int or float):
        """
        Deposits <quantity: int> into the account.
        Raises a ValueError if <quantity> is less than 0.
        """
        if quantity < 0:
            raise ValueError(f"{quantity} is less than 0!")
        self.balance += quantity
        print(f"You have deposited {quantity} to your account.") 

    def print_balance(self):
        """
        Prints the balance of the account.
        """
        print(f"Your current balance is {self.balance}.")
