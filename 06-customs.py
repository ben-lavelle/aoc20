from assets.loader import gather_day, input_day
from requests import get
import re
from functools import reduce

gather_day(6)

with open(input_day(6), 'r') as f:
    answerlists = [re.split(r'\s', group) for group in f.read().strip().split('\n\n')]

### Part 1 ###
coverage = [reduce(lambda p,q: set(p).union(q), group, set()) for group in answerlists]
print(f'Sum of group coverage counts is {sum(len(s) for s in coverage):,}.')

### Part 2 ###
intersects = [reduce(lambda p,q: set(p).intersection(q), group, group[0]) for group in answerlists]
print(f'Sum of group intersection counts is {sum(len(s) for s in intersects):,}.')
