from assets.loader import gather_day, input_day
from requests import get
from itertools import islice

gather_day(3)

with open(input_day(3), 'r') as f:
    frontiers = [l.strip() for l in f.readlines()]
    width = len(frontiers[0])

def hit_me(slope_right: int, slope_down: int = 1):
    new_frontiers = islice(frontiers, 0, None, slope_down)
    collisions = [f[(i * slope_right) % width] == '#' for i, f in enumerate(new_frontiers)]
    print(f'{sum(collisions):,} trees bipped in {len(frontiers):,} frontiers.')
    return sum(collisions)

settings = [(1,1), (3,1), (5,1), (7,1), (1,2)]
answers = [hit_me(*t) for t in settings]

from math import prod
print(f'Product of all bips is {prod(answers):,}')
