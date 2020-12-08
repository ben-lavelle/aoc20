from assets.loader import gather_day, input_day
import re
from collections import namedtuple

gather_day(8)

with open(input_day(8), 'r') as f:
    cmd = re.compile(r'(acc|jmp|nop) ((?:\+|\-)\d{1,4})')
    op = namedtuple('op', ['op', 'i'])
    commands = [op(cmd.match(l)[1], int(cmd.match(l)[2])) for l in f.readlines()
                if cmd.match(l) is not None]

state = namedtuple('state', ['pos', 'acc', 'visited'])
s = state(0, 0, [])
ops = {
    'nop': lambda s, i: state(s.pos + 1, s.acc    , s.visited + [s.pos]),
    'acc': lambda s, i: state(s.pos + 1, s.acc + i, s.visited + [s.pos]),
    'jmp': lambda s, i: state(s.pos + i, s.acc    , s.visited + [s.pos])
}

### Part 1 ###
while s.pos not in s.visited:
    s = ops[commands[s.pos].op](s, commands[s.pos].i)
else:
    print(f'After visiting {len(s.visited):,} commands of {len(commands):,}, '
          f'accumulator stops at {s.acc:,} before revisiting {s.pos}.')

### Part 2 ###
queue, terminates = s.visited.copy(), False
attempts = 0
while not terminates and queue:
    attempts += 1
    idx = queue.pop()
    
    alt_commands = commands.copy()
    switch = {'jmp': 'nop', 'nop': 'jmp', 'acc': 'acc'}
    alt_commands[idx] = op(switch[alt_commands[idx].op], alt_commands[idx].i)
    
    s = state(idx, 0, [])
    while s.pos not in s.visited and s.pos <= len(commands)-1:
        s = ops[alt_commands[s.pos].op](s, alt_commands[s.pos].i)
    else:
        if s.pos > len(commands)-1:
            terminates = True
            print(f'Sequence TERMINATES after {len(s.visited):,} ops from {idx}.')
        else:
            terminates = False
            continue  # Discard this switched command and return to original list.
else:
    if not queue:
        print('FAILED: ran out of queued operations.')
    else:
        print(f'SUCCESS! Found a terminating route after {attempts:,} swaps.')
        print(f'Switching {idx} to {alt_commands[idx]}; restarting traversal...')
        s = state(0, 0, [])
        while s.pos <= len(commands)-1:
            s = ops[alt_commands[s.pos].op](s, alt_commands[s.pos].i)
        else:
            print(f'After visiting {len(s.visited):,} commands of {len(commands):,}, '
                f'accumulator stops at {s.acc:,} before exiting at {s.pos}.')
