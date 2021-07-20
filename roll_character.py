from csv import reader as csv_reader
from random import choice, randint

CHEAT = False
BACKGROUNDS_CSV = 'backgrounds.csv'


def import_backgrounds():
    with open(BACKGROUNDS_CSV) as csvfile:
        rows = list(csv_reader(csvfile))[1:]

    return rows

def is_matching_roll(d100_roll, roll_col_value):
    if str(d100_roll) == roll_col_value:
        return True
    if "-" in roll_col_value:
        min, max = (int(v) for v in roll_col_value.split("-"))
        return min <= d100_roll <= max
    return False

def get_background(d100_roll, backgrounds):
    return [_ for _ in backgrounds if is_matching_roll(d100_roll, _[0])][0]

def get_bonuses(background):
    abilities = ["STR","DEX","CON","WIS","INT","CHA"]
    bonuses = [int(_ or 0) for _ in background[8:14]]

    return ", ".join(f"+{bonus} {abil}" for bonus, abil in zip(bonuses, abilities) if bonus)

def random_alignment(allow_evil=False):
    alignments = ["Lawful Good", "Neutral Good", "Chaotic Good", "Lawful Neutral", "True Neutral", "Chaotic Neutral"]
    if allow_evil:
        alignments += ["Lawful Evil", "Neutral Evil", "Chaotic Evil"]
    return choice(alignments)

def random_race():
    races = ["Dragonborn", "Holder Dwarf", "Rocklit Dwarf", "Dvergar (Dwarf)", "Cloud Elf", "Dark Elf", "Wild Elf", "Firbolg", "Coblygnome", "Maker Gnome", "Pastoral Gnome", "Djogeon (Halfling)", "Mikamwesauk (Halfling)", "Nimerigar (Halfling)", "Human", "Nekomata", "Quinametzin", "Half-elf", "Half-orc", "Hanyou - Pungarehu", "Hanyou - Hukarere", "Hanyou - Faasaunoa", "Wind sagani", "Rain sagani", "Rock sagani", "Fire sagani"]
    return choice(races)

rolls = [sum(sorted(randint(1,6) for _ in range(4))[1:]) for die in range(6)]
rolls = sorted(rolls, reverse=True)
while CHEAT and 18 not in rolls:
    rolls = [sum(sorted(randint(1,6) for _ in range(4))[1:]) for die in range(6)]
total = sum(rolls)
backgrounds = import_backgrounds()
bg_roll = randint(1,100)
background = get_background(bg_roll, backgrounds)
cantrips = background[7]
bonuses = get_bonuses(background)
tool_proficiencies = ", ".join(background[6].split("\n")) if background[6] else None
armor_proficiencies = ", ".join(background[3].split("\n")) if background[3] else None
alignment = random_alignment()

print(f"rolls: {rolls}")
print(f"total: {total}")
print(f"background: {background[1]} ({bg_roll})")
print(f"bonuses: {bonuses}")
if cantrips:
    print(f"cantrips: {cantrips}")
if tool_proficiencies:
    print(f"tool_proficiencies: {tool_proficiencies}")
if armor_proficiencies:
    print(f"armor_proficiencies: {armor_proficiencies}")
print(f"\nalignment: {alignment}")
print(f"race: {random_race()}")
