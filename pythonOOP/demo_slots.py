# demo_slots.py — shows the difference between with and without __slots__

import sys

# --- WITHOUT slots ---
class RegularUser:
    def __init__(self, name, email):
        self.name = name
        self.email = email

# --- WITH slots ---
class SlottedUser:
    __slots__ = ('name', 'email')

    def __init__(self, name, email):
        self.name = name
        self.email = email


u1 = RegularUser("Alice", "a@x.com")
u2 = SlottedUser("Bob", "b@x.com")

# 1. Every normal object has a __dict__
print("1. Does __dict__ exist?")
print("   Regular:", hasattr(u1, '__dict__'))     # True
print("   Slotted:", hasattr(u2, '__dict__'))     # False

# 2. __dict__ is a real dictionary
print("\n2. Content of __dict__ (Regular):")
print("   ", u1.__dict__)                       # {'name': 'Alice', 'email': 'a@x.com'}

# 3. With __slots__ you CANNOT create an attribute outside the list
print("\n3. Try to create extra attribute:")
u1.phone = "9999-0000"                       # works — dynamic attribute
print("   Regular accepted: u1.phone =", u1.phone)

try:
    u2.phone = "9999-0000"                  # AttributeError!
except AttributeError as e:
    print("   Slotted rejected:", e)

# 4. Memory savings (with 100k instances)
print("\n4. Size of ONE instance (sys.getsizeof):")
print("   Regular:", sys.getsizeof(u1), "bytes")
print("   Slotted:", sys.getsizeof(u2), "bytes")

# Average with 100k objects
from time import time

N = 100_000
t0 = time()
regular_objs = [RegularUser(f"u{i}", f"u{i}@x.com") for i in range(N)]
t1 = time()
slotted_objs = [SlottedUser(f"u{i}", f"u{i}@x.com") for i in range(N)]
t2 = time()

print(f"\n5. Creating {N} instances:")
print(f"   Regular: {t1-t0:.2f}s")
print(f"   Slotted: {t2-t1:.2f}s")

# approximate size = size of the list of objects
size_regular = sys.getsizeof(regular_objs) + sum(sys.getsizeof(o) for o in regular_objs[:100])
size_slotted = sys.getsizeof(slotted_objs) + sum(sys.getsizeof(o) for o in slotted_objs[:100])
print(f"\n6. Approximate memory (100 instances):")
print(f"   Regular: ~{size_regular} bytes")
print(f"   Slotted: ~{size_slotted} bytes")
print(f"   Savings: ~{(1 - size_slotted/size_regular)*100:.0f}%")