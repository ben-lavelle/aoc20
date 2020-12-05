from assets.config import USER_SESSION_ID
from requests import get
from collections import namedtuple
import re

response = get('https://adventofcode.com/2020/day/5/input', cookies={'session': USER_SESSION_ID})
if response.ok:
    with open('assets/05-input.txt', 'w') as f:
        f.write(response.text)

with open('assets/05-input.txt', 'r') as f:
    passes = [l.strip() for l in f.readlines()]

def locate(seat: str) -> tuple:
    box = (0, 128, 0, 8)
    loc = namedtuple('loc', ['row', 'column', 'uid'])
    flippers = {
        'B': lambda i,j,m,n: ((i+j)//2, j, m, n),
        'F': lambda i,j,m,n: (i, (i+j)//2, m, n),
        'R': lambda i,j,m,n: (i, j, (m+n)//2, n),
        'L': lambda i,j,m,n: (i, j, m, (m+n)//2)
    }
    for c in seat:
        box = flippers[c](*box)
    return loc(row=box[0], column=box[2], uid=8*box[0]+box[2])

seats = [locate(seat) for seat in passes]
print(f'With {len(passes):,} passes, the max UID is {max(s.uid for s in seats)}.')

### Part 2 ###
occupied = [s.uid for s in seats]
possibles = set(range(max(occupied)))
empties = list(possibles.difference(occupied))
print(empties)