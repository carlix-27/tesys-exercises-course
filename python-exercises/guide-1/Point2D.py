import math

class Point2D:

    maxDistanceToOrigin = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

        distance = Point2D.getDistanceToOrigin(self)

        if distance > Point2D.maxDistanceToOrigin:
            Point2D.maxDistanceToOrigin = distance

    def getDistance(self, point):
        return math.sqrt(
            math.pow(point.x - self.x, 2) +
            math.pow(point.y - self.y, 2)
        )

    def add(self, point):
        return Point2D(self.x + point.x, self.y + point.y)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    @classmethod
    def getDistanceToOrigin(cls, point):
        return math.sqrt(
            math.pow(point.x, 2) +
            math.pow(point.y, 2)
        )


p1 = Point2D(3, 4)
p2 = Point2D(5, 12)
p3 = Point2D(8, 15)

print("Distancia p1 a p2:", p1.getDistance(p2))

sumPoint = p1.add(p2)

print("Nuevo punto:", sumPoint.getX(), sumPoint.getY())

print("Maxima distancia al origen:",
      Point2D.maxDistanceToOrigin)