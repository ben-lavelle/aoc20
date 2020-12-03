from requests import get
from assets.config import USER_SESSION_ID
from itertools import islice

response = get('https://adventofcode.com/2020/day/3/input', cookies={'session': USER_SESSION_ID})
if response.ok:
    with open('assets/03-input.txt', 'w') as f:
        f.write(response.text)

with open('assets/03-input.txt', 'r') as f:
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
