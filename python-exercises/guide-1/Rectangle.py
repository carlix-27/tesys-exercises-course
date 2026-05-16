class Rectangle:

    def __init__(self, b=0, h=0):
        self.base = b
        self.height = h

    def calculateArea(self):
        return self.base * self.height

rectangle1 = Rectangle()

rectangle1.base = 10
rectangle1.height = 5

print("Area Rectangle1:", rectangle1.calculateArea())


rectangle2 = Rectangle(23, 7)

print("Area Rectangle2:", rectangle2.calculateArea())