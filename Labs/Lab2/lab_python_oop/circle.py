import math
from .figure import Figure
from .color import Color


class Circle(Figure):
    name = "Circle"

    def __init__(self, radius, color):
        self.radius = radius
        self.color = Color(color)

    def area(self):
        return math.pi * self.radius ** 2

    def __repr__(self):
        return "{} (Radius: {}, Color: {}, Area: {:.2f})".format(
            self.name, self.radius, self.color.color, self.area()
        )
