import re


class SpecialMethods:
    def __init__(self, value: str):
        self.value = value

    @staticmethod
    def _digits(value: str) -> str:
        return re.sub(r'\D', '', value)

    def __bool__(self):
        digits = SpecialMethods._digits(self.value)
        if len(digits) != 11:
            return False
        return True

    def __repr__(self):
        digits = self._digits(self.value)
        return f"SpecialMethods('{digits}')"

    def __str__(self):
        digits = self._digits(self.value)

        if SpecialMethods.__bool__(self):
            return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"
        return "Invalid CPF"


    def __eq__(self, other):
        if isinstance(other, SpecialMethods):
            return self._digits(self.value) == self._digits(other.value)
        return NotImplemented
        
    def __hash__(self):
        return hash(self._digits(self.value))


def main():
    cpf1 = SpecialMethods("123.456.789-01")
    cpf2 = SpecialMethods("12345678901")
    cpf3 = SpecialMethods("987.654.321-00")

    print(repr(cpf1))  
    print(str(cpf1))
    print(cpf1 == cpf2)
    print(cpf1 == cpf3)

    print(bool(SpecialMethods("123.456.789-01")))
    print(bool(SpecialMethods("")))
    print(bool(SpecialMethods("12345")))

if __name__ == "__main__":
    main()
