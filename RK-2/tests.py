import unittest

from main import get_computers_with_programs_starting_with_a, \
  calculate_average_version, get_programs_ending_with_r, Program, Computer


class TestProgramAnalysis(unittest.TestCase):
  def setUp(self):
    self.computers = [
      Computer(1, 'Alpha Computer'),
      Computer(2, 'Beta Computer'),
      Computer(3, 'Aqua Computer')
    ]

    self.programs = [
      Program(1, 'Text Editor', 'v1.0', 1),
      Program(2, 'Browser', 'v2.1', 2),
      Program(3, 'Media Player', 'v3.5', 3),
      Program(4, 'Image Editor', 'v1.2', 1),
      Program(5, 'Video Editor', 'v4.0', 2)
    ]

  def test_get_programs_ending_with_r(self):
    result = get_programs_ending_with_r(self.programs, self.computers)
    expected = [('Text Editor', 'Alpha Computer'),
                ('Browser', 'Beta Computer'),
                ('Media Player', 'Aqua Computer'),
                ('Image Editor', 'Alpha Computer'),
                ('Video Editor', 'Beta Computer')]
    self.assertEqual(result, expected)

  def test_calculate_average_version(self):
    result = calculate_average_version(self.programs, self.computers)
    expected = [('Alpha Computer', 1.1), ('Beta Computer', 3.05),
                ('Aqua Computer', 3.5)]
    self.assertEqual(result, expected)

  def test_get_computers_with_programs_starting_with_a(self):
    result = get_computers_with_programs_starting_with_a(self.computers,
                                                         self.programs)
    expected = [
      ('Alpha Computer', ['Text Editor', 'Image Editor']),
      ('Aqua Computer', ['Media Player'])
    ]
    self.assertEqual(result, expected)


if __name__ == '__main__':
  unittest.main()
