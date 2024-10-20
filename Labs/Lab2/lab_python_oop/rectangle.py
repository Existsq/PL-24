from .figure import Figure
from .color import Color


class Rectangle(Figure):
    name = "Rectangle"

    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = Color(color)

    def area(self):
        return self.width * self.height

    def __repr__(self):
        return "{} (Width: {}, Height: {}, Color: {}, Area: {})".format(
            self.name, self.width, self.height, self.color.color, self.area()
        )
