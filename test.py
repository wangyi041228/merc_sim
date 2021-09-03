from enum import Enum
RACE = Enum('RACE', ('Tauren', 'Human', 'Orc', 'Beast', 'Demon', 'Murloc', 'Element', 'Night Elf', 'Gnome', 'Undead',
                     'Dwarf', 'Blood Elf', 'Troll', 'High Elf', 'Dragon'))
M_TYPE = Enum('TYPE', 'Protector Fighter Caster')
for name, member in RACE.__members__.items():
    print(name, '=>', member, ',', member.value)
for name, member in M_TYPE.__members__.items():
    print(name, '=>', member, ',', member.value)


for a, b in ((1, 2), (3, 4)):
    print(a, b)
