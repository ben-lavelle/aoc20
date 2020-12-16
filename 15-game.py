from tqdm import tqdm
from collections import defaultdict

starters = [1, 20, 11, 6, 12, 0]

### Part 1 ###
numbers = starters.copy()
while len(numbers) < 2020:
    j = numbers.pop()
    try:
        numbers.extend([j, list(reversed(numbers)).index(j)+1])
    except ValueError:
        numbers.extend([j, 0])

print(f'The 2020th number to be spoken is {numbers[-1]}.')

### Part 2 ###
turns=30000000
lastpos = {1:1, 20:2, 11:3, 6:4, 12:5}
turn, n = 7, 0
pbar = tqdm(total=turns)
while turn <= turns:
    if lastpos.get(n, 0) == 0:
        m = 0
    else:
        m = turn-1 - lastpos[n]
    lastpos[n] = turn-1
    n = m
    turn += 1
    pbar.update()
pbar.close()

print(f'The {turns:,}th number to be spoken is {n:,}.')
