from assets.config import USER_SESSION_ID
from requests import get
import re
from functools import reduce

response = get('https://adventofcode.com/2020/day/6/input', cookies={'session': USER_SESSION_ID})
if response.ok:
    with open('assets/06-input.txt', 'w') as f:
        f.write(response.text)

with open('assets/06-input.txt', 'r') as f:
    answerlists = [re.split(r'\s', group) for group in f.read().strip().split('\n\n')]

### Part 1 ###
coverage = [reduce(lambda p,q: set(p).union(q), group, set()) for group in answerlists]
print(f'Sum of group coverage counts is {sum(len(s) for s in coverage):,}.')

### Part 2 ###
intersects = [reduce(lambda p,q: set(p).intersection(q), group, group[0]) for group in answerlists]
print(f'Sum of group intersection counts is {sum(len(s) for s in intersects):,}.')
