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


computers = [
    Computer(1, 'Alpha Computer'),
    Computer(2, 'Beta Computer'),
    Computer(3, 'Aqua Computer')
]

programs = [
    Program(1, 'Text Editor', 'v1.0', 1),
    Program(2, 'Browser', 'v2.1', 2),
    Program(3, 'Media Player', 'v3.5', 3),
    Program(4, 'Image Editor', 'v1.2', 1),
    Program(5, 'Video Editor', 'v4.0', 2)
]

programs_on_computer = [
    ProgramsOnComputer(1, 1),
    ProgramsOnComputer(2, 2),
    ProgramsOnComputer(3, 3),
    ProgramsOnComputer(4, 1),
    ProgramsOnComputer(5, 2)
]

# 1. Список программ, у которых название заканчивается на "r", и название их компьютеров
programs_with_r = [(p.name, c.name) for p in programs for c in computers if
                   p.computer_id == c.computer_id and p.name.endswith('r')]

print("Программы с названием, заканчивающимся на 'r':")
for program, computer in programs_with_r:
    print(f"Программа: {program}, Компьютер: {computer}")

# 2. Список компьютеров со средней версией программы на каждом компьютере
computer_avg_version = []
for c in computers:
    comp_programs = [p for p in programs if p.computer_id == c.computer_id]
    if comp_programs:
        avg_version = sum([float(p.version.split('v')[1]) for p in comp_programs]) / len(comp_programs)
        computer_avg_version.append((c.name, avg_version))

computer_avg_version.sort(key=lambda x: x[1])

print("\nСредняя версия программ на компьютерах:")
for computer, avg_version in computer_avg_version:
    print(f"Компьютер: {computer}, Средняя версия программы: {avg_version:.2f}")

# 3. Список всех компьютеров, название которых начинается на "A" и список программ на них
computers_with_a = [(c.name, [p.name for p in programs if p.computer_id == c.computer_id]) for c in computers if
                    c.name.startswith('A')]

print("\nКомпьютеры с названием на 'A' и их программы:")
for computer, programs_list in computers_with_a:
    print(f"Компьютер: {computer}, Программы: {', '.join(programs_list) if programs_list else 'Нет программ'}")
