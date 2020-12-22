from assets.loader import gather_day, input_day
import re
from functools import reduce
from itertools import chain
import networkx as nx
from networkx.algorithms import bipartite

gather_day(21)

with open(input_day(21), 'r') as f:
    pattern = re.compile(r'([\w ]+) \(contains ([\w, ]+)\)')
    tuples = [pattern.match(l).groups() for l in f.readlines()]

tokens = [(set(u.split(' ')), set(v.split(', '))) for u,v in tuples]
ingredients, allergens = (reduce(set.union, [u for u,v in tokens]), 
                          reduce(set.union, [v for u,v in tokens]))

could = dict()
for a in allergens:
    apps = reduce(set.intersection, [u for u, v in tokens if a in v])
    if apps:
        could[a] = apps

### Part 1 ###
couldnt = ingredients - reduce(set.union, could.values())
count = sum(1 for i in chain(*[u for u,v in tokens]) if i in couldnt)
print(f'Total occurrances of SAFE ingredients is {count:,}. Yum.')

### Part 2 ###
B = nx.Graph()
B.add_nodes_from(could.keys(), bipartite=0)
B.add_nodes_from(reduce(set.union, could.values()), bipartite=1)
for k, v in could.items():
    B.add_edges_from([(k, j) for j in v])

matching = [(u,v) for u,v in bipartite.maximum_matching(B).items()
            if B.nodes[u]['bipartite'] == 0]
print(f'We have a matching of size {len(matching)}, cf. {len(could.keys())=}.')
print('Our canonical DANGER list is:')
print(','.join(t[1] for t in sorted(matching, key=lambda t: t[0])))
