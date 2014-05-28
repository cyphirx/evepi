import math
from evepi import app

def levelFromSp(sp, rank):
    try:
        skillLevel = math.floor((math.log(sp/(250*rank)) + 2.5) / 2.5)
    except ValueError:
        skillLevel = 0

    if skillLevel > 5:
        skillLevel = 5
    return int(skillLevel)

def spFromLevel(level, rank):
    return 2 ** ((2.5*level) - 2.5) * 250 * rank
# vim: set ts=4 sw=4 et :


