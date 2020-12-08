from assets.loader import gather_day, input_day
from requests import get
import re

gather_day(2)

with open(input_day(2), 'r') as f:
    passwords = [l.strip() for l in f.readlines()]

### Part 1 ###
spec = re.compile(r'(\d{1,2})\-(\d{1,2}) ([a-z])\: ([a-z]{1,100})')
specs = [  (spec.match(p).group(4), # Password
            spec.match(p).group(3), # Char
            int(spec.match(p).group(1)), # LB
            int(spec.match(p).group(2))  # UB
            ) for p in passwords]

def introspec(spec: tuple) -> bool:
    n = spec[0].count(spec[1])
    return n >= spec[2] and n <= spec[3]

checks = [introspec(s) for s in specs]
print(f'{sum(checks):,} of {len(passwords):,} passwords pass introspec spec checks.')

### Part 2 ###
def retrospec(spec: tuple) -> bool:
    i, j = spec[0][spec[2]-1], spec[0][spec[3]-1]
    return sum([i==spec[1], j==spec[1]]) == 1

retrochecks = [retrospec(s) for s in specs]
print(f'{sum(retrochecks):,} of {len(passwords):,} passwords pass retrospec retro spec checks.')
