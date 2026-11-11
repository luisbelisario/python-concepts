# MRO e o problema do diamante

class A:
    def ping(self):
        return "A"

    @staticmethod
    def info():
        return "I am A"

class B(A):
    def ping(self):
        return "B" + super().ping()

class C(A):
    def ping(self):
        return "C" + super().ping()

class D(B, C):
    def ping(self):
        return "D" + super().ping()


print("=== MRO de D ===")
for cls in D.__mro__:
    print(f"  {cls.__name__}")

print()
print("D().ping():", D().ping())  # DBCA

# O que acontece passo a passo:
# 1. D.ping() → "D" + super().ping()
# 2. super() em D vai para B (proximo no MRO)
# 3. B.ping() → "B" + super().ping()
# 4. super() em B vai para C (proximo no MRO, NAO para A!)
# 5. C.ping() → "C" + super().ping()
# 6. super() em C vai para A
# 7. A.ping() → "A"
# Resultado: "D" + "B" + "C" + "A" = "DBCA"

print()
print("=== Metodos com mesmo nome mas SEM super() ==")

class X:
    def ping(self):
        return "X"

class Y:
    def ping(self):
        return "Y"

class Z(X, Y):
    pass

print("Z.__mro__:", [c.__name__ for c in Z.__mro__])
print("Z().ping():", Z().ping())  # "X" — primeiro no MRO vence

print()
print("=== Metodos estaticos ===")
# Static methods seguem a mesma regra de resolucao (MRO)

class ServiceA:
    @staticmethod
    def get_name():
        return "ServiceA"

class ServiceB(ServiceA):
    @staticmethod
    def get_name():
        return "ServiceB"

class ServiceC(ServiceA):
    @staticmethod
    def get_name():
        return "ServiceC"

class ServiceD(ServiceB, ServiceC):
    @staticmethod
    def get_name():
        # super() funciona com staticmethod tambem
        return "ServiceD:" + super(ServiceD, ServiceD).get_name()

print("ServiceD.__mro__:", [c.__name__ for c in ServiceD.__mro__])
print("ServiceD.get_name():", ServiceD.get_name())

# Nota: super() em staticmethod precisa da chamada explicita
# super(Classe, Classe).metodo() em vez de super().metodo()
# Porque staticmethod nao recebe cls nem self