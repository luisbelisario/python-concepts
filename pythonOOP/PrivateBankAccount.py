class PrivateBankAccount:

    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self._balance = balance
        self.__password = "secret123"


    def get_balance(self):
        return self._balance

    def __str__(self):
        return f"{self.owner}', U$ {self._balance})"



def main():
    account = PrivateBankAccount("Alice", 1000.0)
    print(account.owner)

    print(account._balance)

    try:
        print(account.__password)
    except AttributeError as e:
        print(f"Error trying to access private attribute: {e}")

    print(account._PrivateBankAccount__password)

    account._balance = 2000.0
    print(account.get_balance())

    account._PrivateBankAccount__password = "hacked"

    print(account._PrivateBankAccount__password)


if __name__ == "__main__":
    main()