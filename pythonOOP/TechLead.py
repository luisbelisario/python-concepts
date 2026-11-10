from Manager import Manager
from Developer import Developer

class TechLead(Manager, Developer):
    def __init__(self, name: str, base_salary: float, bonus: float):
        super().__init__(name=name, base_salary=base_salary, bonus=bonus)

    def info(self):
        return super().info() + f", Lead: Yes"


def main():
    tech_lead = TechLead("Alice", 10000, 2000)
    print(tech_lead.info())
    print(TechLead.__mro__)

if __name__ == "__main__":
    main()