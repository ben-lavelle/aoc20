from assets.loader import gather_day, input_day
import re
from functools import reduce
from itertools import chain
from collections import defaultdict
import networkx as nx
from networkx.algorithms import bipartite
from math import prod
import matplotlib.pyplot as plt

gather_day(16)

with open(input_day(16), 'r') as f:
    rules, mine, nearby = (p.splitlines() for p in f.read().split('\n\n'))
    mine = [int(n) for n in mine[1].split(',')]
    nearby = [[int(n) for n in l.split(',')] for l in nearby[1:]]

ruler = re.compile(r'([a-z ]+): (\d{2,3})-(\d{2,3}) or (\d{2,3})-(\d{2,3})')
ranges = {ruler.match(r)[1]: tuple(int(k) for k in ruler.match(r).groups()[1:])
          for r in rules}

passable = reduce(lambda t1, t2: t1.union(
    range(t2[0], t2[1]+1)).union(range(t2[2], t2[3]+1)),
    ranges.values(),
    set()
)

### Part 1 ###
errors = sum(i for i in chain(*nearby) if i not in passable)
print(f'Error rate is {errors:,}.')

### Part 2 ###
nearby_slim = [l for l in nearby if all([i in passable for i in l])]
print(f'Slimmed down `nearby` from {len(nearby)} to {len(nearby_slim)}.')
n_rules = len(ranges.keys())
fields = defaultdict(list)
for k, rs in ranges.items():
    k_passable = set(range(rs[0], rs[1]+1)).union(range(rs[2], rs[3]+1))
    for j in range(n_rules):
        if all([nearby_slim[i][j] in k_passable for i in range(len(nearby_slim))]):
            fields[k] += [j]

print(f'Most restrictive field has {min(len(l) for l in fields.values())}.')

# Let's make a bipartite graph and find a covering matching.
B = nx.Graph()
B.add_nodes_from(fields.keys(), bipartite=0)
B.add_nodes_from(range(n_rules), bipartite=1)
for k, v in fields.items():
    B.add_edges_from([(k, j) for j in v])

matching = bipartite.maximum_matching(B)
# Matching returns double-dictionary of field:num and num:field so halve length.
print(f'We have a matching of size {len(matching)/2}, cf. {n_rules=}.')
print('We find:')
print('\n'.join([str(i) for i in matching.items() if isinstance(i[0], str)]))

departure_fields = [v for k, v in matching.items()
                    if isinstance(k, str)
                    and k[:9] == 'departure']
print('Product of my departure fields is '
      f'{prod(mine[i] for i in departure_fields):}.')

# Out of interest, how does it look? (Run in Jupyter)
colors = [('grey', 'red')[e in matching.items()] for e in B.edges()]
nx.draw(B, pos=nx.layout.bipartite_layout(B, [n[0] for n in B.nodes(data='bipartite') if n[1]==0]),
        with_labels=True, edge_color=colors)
plt.show()
