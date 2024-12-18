class Program:
  def __init__(self, program_id, name, version, computer_id):
    self.program_id = program_id
    self.name = name
    self.version = version
    self.computer_id = computer_id


class Computer:
  def __init__(self, computer_id, name):
    self.computer_id = computer_id
    self.name = name


class ProgramsOnComputer:
  def __init__(self, program_id, computer_id):
    self.program_id = program_id
    self.computer_id = computer_id


def get_programs_ending_with_r(programs, computers):
  return [
    (p.name, c.name)
    for p in programs
    for c in computers
    if p.computer_id == c.computer_id and p.name.endswith('r')
  ]


def calculate_average_version(programs, computers):
  result = []
  for c in computers:
    comp_programs = [p for p in programs if p.computer_id == c.computer_id]
    if comp_programs:
      avg_version = sum(
          [float(p.version.split('v')[1]) for p in comp_programs]) / len(
          comp_programs)
      result.append((c.name, avg_version))
  result.sort(key=lambda x: x[1])
  return result


def get_computers_with_programs_starting_with_a(computers, programs):
  return [
    (c.name, [p.name for p in programs if p.computer_id == c.computer_id])
    for c in computers if c.name.startswith('A')
  ]
