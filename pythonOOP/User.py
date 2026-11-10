class User:

    total_users = 0

    def __init__(self, name: str):
        self.name = name
        User.total_users += 1
        self.id = User.total_users
        

    @classmethod
    def list_all(cls):
        return f"Total users registered: {cls.total_users}"

    def rename(self, new_name):
        self.name = new_name

def main():
    user1 = User("Alice")
    user2 = User("Bob")
    print(user1.name)  # Output: Alice
    print(user2.name)  # Output: Bob
    print(User.list_all())  # Output: Total users registered: 2

    user1.rename("Alicia")
    print(user1.name)  # Outpt: Alicia


if __name__ == "__main__":
    main()