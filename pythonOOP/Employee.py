class Employee:
    def __init__(self, name, position, base_salary):
        self._name = name
        self._position = position
        self._base_salary = base_salary

    @property
    def base_salary(self):
        return self._base_salary

    @base_salary.setter
    def base_salary(self, value):
        if value < 0:
            raise ValueError("Base salary cannot be negative.")
        self._base_salary = value

    @property
    def annual_salary(self):
        return self._base_salary * 12

    def raise_salary(self, percentage):
        if percentage < 0:
            raise ValueError("Raise percentage cannot be negative.")
        self.base_salary = self._base_salary * (1 + percentage / 100)
        print(f"Salary raised by {percentage}%. New base salary: {self._base_salary}, New annual salary: {self.annual_salary}")
        


def main():
    emp1 = Employee("John Doe", "Software Engineer", 5000)
    print(f"Employee: {emp1._name}, Position: {emp1._position}, Base Salary: {emp1.base_salary}, Annual Salary: {emp1.annual_salary}")

    
    emp1.base_salary = 5500
    print(f"Updated Base Salary: {emp1.base_salary}, Updated Annual Salary: {emp1.annual_salary}")

    try:
        emp1.base_salary = -1000  # This will raise a ValueError
    except ValueError as e:
        print(e)

    print(emp1.annual_salary)
    
    try:
        emp1.annual_salary = 60000  # AttributeError: can't set attribute
    except AttributeError as e:
        print(e)

    emp1.raise_salary(10)


if __name__ == "__main__":
    main()