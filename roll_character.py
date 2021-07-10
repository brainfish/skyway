from csv import reader as csv_reader
from random import randint

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

rolls = [sum(sorted(randint(1,6) for _ in range(4))[1:]) for die in range(6)]
while CHEAT and 18 not in rolls:
    rolls = [sum(sorted(randint(1,6) for _ in range(4))[1:]) for die in range(6)]
total = sum(rolls)
backgrounds = import_backgrounds()
bg_roll = randint(1,100)
background = get_background(bg_roll, backgrounds)
cantrips = background[7]
bonuses = get_bonuses(background)

print(f"rolls: {rolls}")
print(f"total: {total}")
print(f"background: {background[1]} ({bg_roll})")
print(f"bonuses: {bonuses}")
if cantrips:
    print(f"cantrips: {cantrips}")
