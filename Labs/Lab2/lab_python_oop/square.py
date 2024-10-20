from .rectangle import Rectangle


class Square(Rectangle):
    name = "Square"

    def __init__(self, side, color):
        super().__init__(side, side, color)

    def __repr__(self):
        return "{} (Side: {}, Color: {}, Area: {})".format(
            self.name, self.width, self.color.color, self.area()
        )
