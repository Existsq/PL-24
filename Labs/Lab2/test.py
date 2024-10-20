import unittest
from lab_python_oop.rectangle import Rectangle


class TestRectangle(unittest.TestCase):
    def test_area(self):
        rect = Rectangle(4, 5, "green")
        self.assertEqual(rect.area(), 20)

    def test_zero_area(self):
        rect = Rectangle(0, 5, "green")
        self.assertEqual(rect.area(), 0)


if __name__ == "__main__":
    unittest.main()
