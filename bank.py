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
    def __init__(self, name: str, balance: int or float, account_number: int):
        self.name = name
        self.balance = balance
        self.account_number = account_number

    def withdraw(self, quantity: int or float):
        if self.balance >= quantity:
            self.balance -= quantity
            print(f"You have successfully withdrawn {quantity} from your account.")
        else:
            raise ValueError(f"You don't have enough money in your account to withdraw {quantity}!")
    
    def deposit(self, quantity: int or float):
        self.balance += quantity
        print(f"You have deposited {quantity} to your account.")

    def print_balance(self):
        print(f"Your current balance is {self.balance}.")
