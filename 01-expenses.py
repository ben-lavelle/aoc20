from assets.loader import gather_day, input_day
from requests import get
from collections import deque
from time import sleep

gather_day(1)

with open(input_day(1), 'r') as f:
    expenses = [int(l) for l in f.readlines()]

### Part 1 ###
target = 2020
solution = tuple()
queue = deque(sorted(expenses))
little, large, i = queue.popleft(), queue.pop(), 0
while not solution and queue:
    i+=1
    if little + large > target:
        large = queue.pop()
    elif little + large < target:
        little = queue.popleft()
    else: 
        solution = (little, large)

print(f'Found {solution=} in {i:,} comparisons from a list of {len(expenses):,} expenses ({len(queue):,} remain untouched).')
print(f'Submit: {little*large=:,}')

### Part 2 ###
from random import sample
from time import sleep
from collections import deque
target = sum(sample(expenses, 3))
print(f'Target is {target:,}.')
queue = deque(sorted(expenses))
little, middle, large = queue.popleft(), queue.popleft(), queue.pop()
print(f'Considering ({little:>6,},  {middle:>6,},  {large:>6,}) (sum {little+middle+large:,})...', end='\r', flush=True)
i = 3
solution = tuple()
while not solution and queue:
    if little + middle + large > target:
        # (Two smallest + large) too big -> large too big
        large = queue.pop()
        i+=1
        print(f'Considering ({little:>6,}, {middle:>6,}, *{large:>5,}) (sum {little+middle+large:,})...', end='\r', flush=True)
        sleep(0.1)
        continue
    elif little + middle + large < target:
        if little + queue[-1] + large < target:
            # (Two largest + small) too small -> smallest too small [save flipping through all the in-betweens]
            little = middle
            middle = queue.popleft()
            print(f'Considering (*{little:>5,}, *{middle:>5,}, {large:>6,}) (sum {little+middle+large:,})...', end='\r', flush=True)
            sleep(0.1)
            continue
        middles = queue.copy()
        temp_mid = 0
        while little + temp_mid + large < target:
            # Step through the in-betweens until the sum is too big.
            temp_mid = middles.popleft()
            print(f'Considering ({little:>6,}, *{temp_mid:>5,}, {large:>6,}) (sum {little+temp_mid+large:,})...', end='\r', flush=True)
            sleep(0.1)
            i+=1
        if little + temp_mid + large == target:
            middle = temp_mid
            continue
        else:
            # If middles iterations go (too small, too small, too big) then large must be too large
            # This made sense at the time but is there a hole if mid/large are fine but little needs to increase?
            large = queue.pop()
            print(f'Considering ({little:>6,}, {middle:>6,}, *{large:>5,}) (sum {little+middle+large:,})...', end='\r', flush=True)
            sleep(0.1)
            continue
    else:
        print(f'Considering ({little:>6,}, {middle:>6,}, {large:>6,}) (sum {little+middle+large:,})..!!!!', flush=True)
        solution = (little, middle, large)

from math import comb
sleep(3)
print(f'Found {solution=} in {i:,} comparisons from a list of {len(expenses):,} expenses (all comparisons {comb(200,3):,}).')
print(f'Submit: {little*middle*large=:,}.')
