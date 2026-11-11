# Python OOP — Quick Reference

## 1. Classes, __init__, self
- `self` is **explicit** — every attribute access needs `self.attr`
- Forgetting `self` in `__init__` = local variable, no attribute created (no error!)
- Python: `def method(self, arg):` — Java: `public void method(Type arg)`

## 2. Instance vs Class Attributes

### Lookup rule
Read: instance → class → base classes
Write (`self.x = val`): **always creates on instance** (never touches class)

### Shared attribute — the trap
```python
class Dog:
    tricks = []          # class attribute — ONE list for ALL dogs

d1 = Dog()
d2 = Dog()
d1.tricks.append("roll")  # mutates the SHARED list
d2.tricks.append("sit")   # same list
print(d1.tricks)  # ['roll', 'sit'] — both dogs see each other's tricks!
```

### Each-instance attribute (correct)
```python
class Dog:
    def __init__(self):
        self.tricks = []  # instance attribute — each dog gets its own

d1 = Dog()
d2 = Dog()
d1.tricks.append("roll")
d2.tricks.append("sit")
print(d1.tricks)  # ['roll']
print(d2.tricks)  # ['sit']
```

### Immutable class attributes are safe
```python
class Config:
    VERSION = "1.0"    # immutable (str) — safe to share

Config.VERSION = "2.0"  # modifies class attribute
c = Config()
print(c.VERSION)        # "2.0" — reads from class
c.VERSION = "3.0"       # CREATES instance attribute, shadows class one
print(Config.VERSION)   # "2.0" — untouched
print(c.VERSION)        # "3.0" — instance attribute
```

### Common Java dev mistake
Putting `[]`/`{}`/`set()` in class body thinking each instance gets its own.
They don't — move to `__init__`.

## 3. @classmethod vs @staticmethod

### What each receives
| Decorator | Receives | Can access |
|-----------|----------|------------|
| `@classmethod` | `cls` (the class) | Class attributes, factory methods |
| `@staticmethod` | Nothing | Nothing — just a function in the class |

### Example: factory (@classmethod) + validator (@staticmethod)
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def create_anonymous(cls):           # cls = Person (or a subclass)
        """Returns a Person with default values"""
        return cls("Anonymous", 0)       # uses cls, not Person

    @staticmethod
    def is_adult(age):                   # receives nothing
        """Returns True if age >= 18"""
        return age >= 18


# Usage
p = Person.create_anonymous()
print(p.name, p.age)       # Anonymous 0
print(Person.is_adult(20))  # True
print(Person.is_adult(15))  # False
```

### Why `cls` instead of `Person`? (polymorphism)
```python
class Employee(Person):
    pass

e = Employee.create_anonymous()   # cls = Employee → returns Employee
print(type(e).__name__)          # Employee
```
With `Person` hardcoded, `create_anonymous` would return a `Person` even when called on `Employee`. That's the bug `cls` prevents.

### The hardcoding trap (from our exercises)
```python
@classmethod
def add_to_catalog(cls, book):
    Book._catalog.append(book)   # HARDCODED — if called on Ebook, still writes to Book
```
Use `cls._catalog` instead.

### When to use each
- `@classmethod` → factory methods (`from_json()`, `from_csv()`, `load()`), alternate constructors, anything that needs the class
- `@staticmethod` → validation helpers, utility functions that logically belong inside the class but need no class/instance data

### Java comparison
Java has one `static`. Python splits into: `@classmethod` (gets the class, polymorphic) and `@staticmethod` (gets nothing, not polymorphic). If you're translating a Java `static` factory method, use `@classmethod`.

## 4. @property (getter/setter/deleter)

- `obj.x` → calls getter; `obj.x = v` → calls setter
- **Uniform access principle:** start with a public attribute, add `@property` later — no API break
- Inside the class, use `self.x = v` (goes through setter), not `self._x = v`
- Read-only property = no setter → `obj.x = v` raises `AttributeError`

### Example: Employee with validated salary
```python
class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self._base_salary = base_salary  # private backing field

    @property
    def base_salary(self):               # getter — read like an attribute
        return self._base_salary

    @base_salary.setter
    def base_salary(self, value):        # setter — validates on assignment
        if value < 0:
            raise ValueError("Salary cannot be negative")
        self._base_salary = value

    @property
    def annual_salary(self):             # read-only (no setter) — computed
        return self._base_salary * 12


# Usage — looks like plain attributes
e = Employee("Alice", 5000)
print(e.base_salary)        # 5000   — calls getter
e.base_salary = 5500        # calls setter, validates
print(e.annual_salary)      # 66000  — calls read-only property

# e.annual_salary = 70000   # AttributeError: can't set attribute
# e.base_salary = -100      # ValueError: Salary cannot be negative
```

### Uniform access principle
Start with a public attribute `emp.salary`, then add `@property` later — code that uses `emp.salary` still works. No getter/setter methods to break.

## 5. __slots__

### What is __dict__?
Every Python object normally carries a dictionary (`__dict__`) that maps attribute names to values. This is what allows `obj.anything = x` to work at any time. But each dictionary costs ~300 bytes of extra memory per instance.

### What __slots__ does
`__slots__ = ("x", "y")` tells Python: "this class only has these attributes, allocate fixed space for them." The `__dict__` is eliminated entirely.

**Savings:** ~288 bytes per instance. In 1 million objects → ~275 MB saved.
**Speed:** Attribute access is also slightly faster (dictionary lookup skipped).

### Trade-off
- ✅ Saves memory, faster attribute access
- ❌ Cannot add attributes outside the list (`obj.z = 1` → `AttributeError`)
- ❌ No `__dict__` → no `pickle` by default, no `vars(obj)`
- ❌ Cannot use `__weakref__` unless explicitly listed

### When to use
- **Yes:** Millions of objects with the same set of attributes — ORM rows, telemetry events, 3D points, game entities, cache records
- **No:** Few objects, or you need dynamic attributes somewhere

### When NOT to use (even with many objects)
If you ever need to monkey-patch, add metadata dynamically, or serialize with `pickle`, `__slots__` gets in the way. Default classes are fine for most code.

## 6. Dataclasses (@dataclass, field, frozen)

- Auto-generates `__init__`, `__repr__`, `__eq__`, `__hash__` from type annotations
- `frozen=True` → immutable (like Java `record`)
- `__post_init__` → validation after auto-generated `__init__`
- `field(default=...)` → custom defaults, exclude from repr, etc.
- Python's Lombok. Stop writing boilerplate.

### Example: Order item
```python
from dataclasses import dataclass, field

@dataclass
class OrderItem:
    product: str
    quantity: int
    unit_price: float

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price


# Usage
item = OrderItem("Laptop", 2, 3500.0)
print(item)               # OrderItem(product='Laptop', quantity=2, unit_price=3500.0)
print(item.total)         # 7000.0
print(item == OrderItem("Laptop", 2, 3500.0))  # True (__eq__ auto)
```

### Frozen (immutable)
```python
@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
# p.x = 3.0  # FrozenInstanceError: cannot assign to field 'x'
```

### field() options
```python
@dataclass
class Config:
    host: str = "localhost"          # default: imutavel
    port: int = 8080
    password: str = field(repr=False) # escondido do print/repr
    metadata: dict = field(default_factory=dict)  # mutavel → factory
    id: int = field(compare=False)    # ignorado no ==
    total: float = field(init=False)  # nao recebido no __init__, calculado depois
```

**Regra de ouro:** `default` para imutáveis (int, str, bool), `default_factory` para mutáveis (list, dict, set).

```python
# metadata vira um dict vazio pra CADA instancia
c1 = Config()
c2 = Config()
c1.metadata["env"] = "production"
print(c2.metadata)  # {} — isolado, sem factory isso vazaria
```

## 7. Inheritance, super(), MRO

- Single inheritance = works like Java
- Multiple inheritance = allowed. MRO (C3 linearization) resolves method order
- `super()` is **cooperative** — calls the **next in MRO chain**, not the direct parent
- If one class in the chain forgets `super()`, the rest silently never run
- Check order: `ClassName.__mro__`

### Diamond problem — solved by MRO
```python
class A:
    def ping(self): return "A"

class B(A):
    def ping(self): return "B" + super().ping()

class C(A):
    def ping(self): return "C" + super().ping()

class D(B, C):
    def ping(self): return "D" + super().ping()

print(D.__mro__)  # D → B → C → A → object
print(D().ping()) # "DBCA" — A executado uma vez
```
`super()` in B goes to C (next in MRO), **not** to A.

## 8. Special Methods (__str__, __repr__, __eq__, __hash__, __bool__)
- `__repr__` → dev-facing. Should recreate the object (`Class('args')`)
- `__str__` → user-facing. Falls back to `__repr__`
- `__eq__` and `__hash__` → **must use the same canonical attribute** or sets/dicts break silently
- Define `__eq__` → also define `__hash__`, or object becomes unhashable
- `is` = identity (same object), `==` = value (calls `__eq__`)
- `__bool__` → controls `if obj:`. Fallback to `__len__`, then `True`

## 9. Encapsulation: _, __, name mangling
- `_attr` → convention. "Internal, please don't touch." Nothing stops access.
- `__attr` → name mangling: becomes `_ClassName__attr`. Prevents **accidental collision** in subclasses, not security
- `obj._ClassName__attr` works — real privacy doesn't exist
- Java's `private` doesn't exist in Python. Trust the developer.