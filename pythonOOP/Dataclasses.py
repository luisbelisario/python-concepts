from dataclasses import dataclass


@dataclass
class OrderItem:
    product: str
    quantity: int
    unit_price: float

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if self.unit_price < 0:
            raise ValueError("Unit price cannot be negative.")

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price


def main():
    item1 = OrderItem("Laptop", 2, 3500.00)
    print(item1.total)
    try:
        item2 = OrderItem("Mouse", 0, 50.00)
    except ValueError as e:
        print(e)
    print(repr(item1))
    item3 = OrderItem("Laptop", 2, 3500.00)
    print(item1 == item3) #True
    print(item1 is item3) #False


if __name__ == "__main__":
    main()