class BankAccount:
    def __init__(self, holder, initial_balance=0):
        self.holder = holder
        self.balance = initial_balance
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposit of ${amount:.2f} successful.")
        else:
            print("Invalid deposit amount.")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"Withdrawal of ${amount:.2f} successful.")
        else:
            print("Insufficient balance.")

    def statement(self) -> str:
        return f"Holder: {self.holder}, Balance: ${self.balance:.2f}"


def main():
    account1 = BankAccount("John", 100)
    account1.deposit(50)
    account1.withdraw(200) # error
    print(account1.statement())
    account1.deposit(-20) # error
    account1.withdraw(30)
    print(account1.statement())


if __name__ == "__main__":
    main()