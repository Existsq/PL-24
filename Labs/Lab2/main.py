import math

from lab_python_oop.rectangle import Rectangle
from lab_python_oop.square import Square
from lab_python_oop.circle import Circle


def main():
    N = 5
    rect = Rectangle(N, N, "blue")
    print(rect)

    square = Square(N, "red")
    print(square)

    circle = Circle(N, "green")
    print(circle)

    print(math.pi)


if __name__ == "__main__":
    main()
