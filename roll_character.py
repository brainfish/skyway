from csv import reader as csv_reader
from dataclasses import dataclass, field
from random import choice, randint

BACKGROUNDS_CSV = 'backgrounds.csv'

BASE_REQUIREMENTS = [
        lambda char: char.total >= 70,
]

REQUIREMENTS = [
        lambda char: char.total > 82,
        lambda char: max(char.rolls) >= 17,
        #lambda char: max(char.rolls) >= 18,
        lambda char: "INT" in char.bonuses,
        #lambda char: "DEX" in char.bonuses,
        #lambda char: "STR" in char.bonuses,
        #lambda char: "CON" in char.bonuses,
        #lambda char: "CHA" in char.bonuses,
        lambda char: "Medium" in char.armor_proficiencies,
        #lambda char: "Heavy" in char.armor_proficiencies,
        #lambda char: "word" in char.weapon_proficiencies,
        #lambda char: "Druid" in char.cantrips,
        #lambda char: "Hermit" in char.background,
        #lambda char: ('Pegasus' in char.equipment) or ('Hippogryph' in char.equipment),
]
MAX_ATTEMPTS = 10**3


@dataclass
class Character:
    rolls: list = field(default_factory=list)
    total: int = 0
    background: str = ""
    cantrips: str = ""
    bonuses: str = ""
    tool_proficiencies: str = ""
    weapon_proficiencies: str = ""
    armor_proficiencies: str = ""
    skill_proficiencies: str = ""
    languages: str = ""
    equipment: str = ""
    alignment: str = ""
    race: str = ""


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

def check_all(funcs, value):
    return all(map(lambda func: func(value), funcs))

def print_character(char):
    print(f"rolls: {char.rolls}")
    print(f"total: {char.total}")
    print(f"background: {char.background}")
    print(f"bonuses: {char.bonuses}")
    if char.cantrips:
        print(f"cantrips: {char.cantrips}")
    if char.tool_proficiencies:
        print(f"tool_proficiencies: {char.tool_proficiencies}")
    if char.weapon_proficiencies:
        print(f"weapon_proficiencies: {char.weapon_proficiencies}")
    if char.armor_proficiencies:
        print(f"armor_proficiencies: {char.armor_proficiencies}")
    print(f"\nalignment: {char.alignment}")
    print(f"race: {char.race}")
    print(f"equipment: {char.equipment}")


backgrounds = import_backgrounds()

char_successful = False
char_creations = 0
while not char_successful and char_creations < MAX_ATTEMPTS:
    character = Character()
    rolls = [sum(sorted(randint(1,6) for _ in range(4))[1:]) for die in range(6)]
    character.rolls = sorted(rolls, reverse=True)
    character.total = sum(rolls)

    bg_roll = randint(1,100)
    raw_background = get_background(bg_roll, backgrounds)

    character.background = f"{raw_background[1]} ({bg_roll})"
    character.cantrips = raw_background[7]
    character.bonuses = get_bonuses(raw_background)
    character.tool_proficiencies = ", ".join(raw_background[6].split("\n")) if raw_background[6] else ""
    character.armor_proficiencies = ", ".join(raw_background[3].split("\n")) if raw_background[3] else ""
    character.weapon_proficiencies = ", ".join(raw_background[2].split("\n")) if raw_background[2] else ""
    character.skill_proficiencies = ", ".join(raw_background[5].split("\n")) if raw_background[5] else ""
    character.alignment = random_alignment()
    character.race = random_race()
    character.equipment = " ".join(raw_background[14].split("\n")) if raw_background[14] else ""

    if not check_all(BASE_REQUIREMENTS, character):
        continue

    char_creations += 1
    if check_all(REQUIREMENTS, character):
        char_successful = True

if char_successful:
    print_character(character)
    print(f"\n{char_creations} creation attempts")
else:
    print(f"Unsuccessful after {char_creations} creation attempts")

