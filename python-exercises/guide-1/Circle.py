# =========================
# EJERCICIO 4 - Circle
# =========================

import math

import Point2D

class Circle:

    def __init__(self, center, radius):
        self._center = center
        self.radius = radius

    def center(self):
        return self._center

    def area(self):
        return math.pi * (self.radius ** 2)

    def perimeter(self):
        return 2 * math.pi * self.radius

    def contains(self, point):

        distance = self._center.getDistance(point)

        return distance <= self.radius


center = Point2D(0, 0)

circle = Circle(center, 5)

pointInside = Point2D(3, 4)
pointOutside = Point2D(10, 10)

print("Centro:", circle.center().getX(),
      circle.center().getY())

print("Area:", circle.area())

print("Perimetro:", circle.perimeter())

print("Punto dentro:",
      circle.contains(pointInside))

print("Punto fuera:",
      circle.contains(pointOutside))