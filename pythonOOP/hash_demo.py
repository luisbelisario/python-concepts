print("=" * 60)
print("1. SEM __hash__ — erro na hora de criar set/dict")
print("=" * 60)

class CPF_NoHash:
    def __init__(self, numero):
        self._digits = numero

    def __eq__(self, other):
        return self._digits == other._digits

    def __repr__(self):
        return f"CPF({self._digits})"


c1 = CPF_NoHash("12345678901")
c2 = CPF_NoHash("12345678901")

print(f"c1 == c2: {c1 == c2}")       # True

try:
    s = {c1, c2}
    print(f"Set criado: {s}")
except TypeError as e:
    print(f"ERRO ao criar set: {e}")

print()


print("=" * 60)
print("2. HASH INCONSISTENTE")
print("   c1 == c2 True, mas hash(c1) != hash(c2)")
print("=" * 60)

class CPF_BadHash:
    def __init__(self, numero):
        self.raw = numero

    def __eq__(self, other):
        return self._digits() == other._digits()

    def _digits(self):
        return "".join(d for d in self.raw if d.isdigit())

    def __hash__(self):
        return hash(self.raw)

    def __repr__(self):
        return f"CPF({self.raw})"


c1 = CPF_BadHash("123.456.789-01")
c2 = CPF_BadHash("12345678901")

print(f"c1 == c2: {c1 == c2}")
print(f"hash(c1): {hash(c1)}")
print(f"hash(c2): {hash(c2)}")

s = {c1, c2}
print(f"len(set): {len(s)}  <- esperado 1, mas tem {len(s)} elementos!")
print(f"Set: {s}")
print()

print("-- Busca que falha --")
procurado = CPF_BadHash("12345678901")
print(f"'{procurado}' in set? {procurado in s}")
print()


print("=" * 60)
print("3. HASH CORRETO — tudo funciona")
print("=" * 60)

class CPF_GoodHash:
    def __init__(self, numero):
        self.raw = numero

    def __eq__(self, other):
        return self._digits() == other._digits()

    def _digits(self):
        return "".join(d for d in self.raw if d.isdigit())

    def __hash__(self):
        return hash(self._digits())

    def __repr__(self):
        return f"CPF({self.raw})"


c1 = CPF_GoodHash("123.456.789-01")
c2 = CPF_GoodHash("12345678901")

print(f"c1 == c2: {c1 == c2}")
print(f"hash(c1): {hash(c1)}")
print(f"hash(c2): {hash(c2)}")

s = {c1, c2}
print(f"len(set): {len(s)}  <- 1, como esperado")
print(f"Set: {s}")

procurado = CPF_GoodHash("12345678901")
print(f"'{procurado}' in set? {procurado in s}")

cadastro = {CPF_GoodHash("12345678901"): "Alice"}
print(f"Cadastro[12345678901]: {cadastro[CPF_GoodHash('123.456.789-01')]}")