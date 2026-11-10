class Broken:
    def __init__(self, val):
        self.val = val
    def __eq__(self, other):
        return self.val == other.val

b1 = Broken(1)
b2 = Broken(1)
print("b1 == b2:", b1 == b2)

try:
    s = {b1, b2}
except TypeError as e:
    print("Erro ao criar set:", e)

print()

class Fixed:
    def __init__(self, val):
        self.val = val
    def __eq__(self, other):
        return self.val == other.val
    def __hash__(self):
        return hash(self.val)

f1 = Fixed(1)
f2 = Fixed(1)
s = {f1, f2}
print("f1 == f2:", f1 == f2)
print("len(set):", len(s))
print("Fixed(1) in set:", Fixed(1) in s)


class CPF:
    def __init__(self, number):
        self._digits = number
    def __eq__(self, other):
        return self._digits == other._digits
    def __hash__(self):
        return hash(self._digits)

cpfs = {
    CPF("12345678901"): "Alice",
    CPF("98765432100"): "Bob"
}
print()
print("Dict por CPF:")
print("  CPF 12345678901 ->", cpfs[CPF("12345678901")])
print("  CPF 98765432100 ->", cpfs[CPF("98765432100")])