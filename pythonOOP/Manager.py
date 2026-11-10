from Employee import Employee

class Manager(Employee):


    def __init__(self, name, base_salary, bonus, **kwargs):
        super().__init__(name=name, base_salary=base_salary, **kwargs)
        self.bonus = bonus

    def info(self):
        return super().info() + f", Bonus: {self.bonus}"