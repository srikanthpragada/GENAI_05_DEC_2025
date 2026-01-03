#  Create a class Account to repsent a savings account with acno, customer, balance
#  and provide method like deposit, withdraw and getbalance and also provide __str__ and __eq__

class Account:
    def __init__(self, acno, customer, balance=0):
        self.acno = acno
        self.customer = customer
        self.balance = balance

    def deposit(self, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount must be a positive number")
        self.balance += amount
        return True

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def get_balance(self):
        return self.balance

    def __str__(self):
        return f"Account No: {self.acno}, Customer: {self.customer}, Balance: {self.balance}"

    def __eq__(self, other):
        if isinstance(other, Account):
            return self.acno == other.acno and self.customer == other.customer
        return False
