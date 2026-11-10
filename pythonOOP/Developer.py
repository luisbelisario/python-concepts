from Employee import Employee

class Developer(Employee):


    def __init__(self, name, base_salary, **kwargs):
        super().__init__(name=name, base_salary=base_salary, **kwargs)

    def info(self):
        return super().info() + f", Role: Developer"