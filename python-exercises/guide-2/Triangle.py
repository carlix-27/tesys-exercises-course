import math


# TODO: refinar esto.

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def length(self):
        return math.sqrt(
            (self.p2.x - self.p1.x) ** 2 +
            (self.p2.y - self.p1.y) ** 2
        )
    


class Triangle:
    def __init__(self, l1, l2, l3):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3

    def perimeter(self):
        return (
            self.l1.length() +
            self.l2.length() +
            self.l3.length()
        )

    def isValid(self):
        a = self.l1.length()
        b = self.l2.length()
        c = self.l3.length()

        return (
            a + b > c and
            a + c > b and
            b + c > a
        )

    def area(self):
        if not self.isValid():
            return 0

        a = self.l1.length()
        b = self.l2.length()
        c = self.l3.length()

        s = self.perimeter() / 2

        return math.sqrt(
            s * (s - a) * (s - b) * (s - c)
        )

    def isEquilateral(self):
        a = self.l1.length()
        b = self.l2.length()
        c = self.l3.length()

        return a == b == c

    def isIsoceles(self):
        a = self.l1.length()
        b = self.l2.length()
        c = self.l3.length()

        return (
            a == b or
            a == c or
            b == c
        )

    def isScalane(self):
        a = self.l1.length()
        b = self.l2.length()
        c = self.l3.length()

        return a != b and b != c and a != c


# Uso:
p1 = Point(0, 0)
p2 = Point(3, 0)
p3 = Point(0, 4)

l1 = Line(p1, p2)
l2 = Line(p2, p3)
l3 = Line(p3, p1)

triangle = Triangle(l1, l2, l3)

print(triangle.perimeter())
print(triangle.area())