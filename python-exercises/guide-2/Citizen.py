class Citizen:

    def __init__(self, dni, name, surname, age):
        self.dni = dni
        self.name = name
        self.surname = surname
        self.age = age

    def __eq__(self, other):
        return self.age == other.age

    def __lt__(self, other):
        return self.age < other.age

    def __le__(self, other):
        return self.age <= other.age

    def __gt__(self, other):
        return self.age > other.age

    def __ge__(self, other):
        return self.age >= other.age
    

c1 = Citizen(
    "12345678",
    "Juan",
    "Perez",
    25
)

c2 = Citizen(
    "87654321",
    "Ana",
    "Gomez",
    30
)

print(c1 < c2)
print(c1 > c2)
print(c1 == c2)