from assets.config import USER_SESSION_ID
from requests import get
import re
import networkx as nx
from networkx.algorithms.components import node_connected_component
from networkx.algorithms.tree.recognition import is_tree
from networkx.algorithms.traversal.depth_first_search import dfs_tree, dfs_edges
from networkx.algorithms.simple_paths import all_simple_edge_paths
from math import prod


response = get('https://adventofcode.com/2020/day/7/input', cookies={'session': USER_SESSION_ID})
if response.ok:
    with open('assets/07-input.txt', 'w') as f:
        f.write(response.text)

with open('assets/07-input.txt', 'r') as f:
    bagrules = [l.strip() for l in f.readlines()]

def rule_to_edges(rule: str) -> list:
    """
    Create directed edges of the type bag1 -> bag2; nBags=N
    to indicate bag1 contains N bag2 bags.
    """
    pattern = re.compile(r'([a-z ]+) bags contain ' +
                         4 * r'(?:(\d+) ([a-z ]+) bags?(?:, |\.))?')
    if not pattern.fullmatch(rule):
        return []
    links = []
    groups = list(pattern.fullmatch(rule).groups())
    outer_bag = groups.pop(0)
    while groups and groups[0] is not None:
        links.append((outer_bag, groups.pop(1), {'nBags': int(groups.pop(0))}))
    return links

# Form Graph:
# bag1 --N-> bag2 if bag1 contains N copies of bag2
edges = []
[edges.extend(rule_to_edges(r)) for r in bagrules]
nodes = list(set(re.findall('([a-z]+ [a-z]+) bags?', ' '.join(bagrules))))

G = nx.DiGraph(nodes=nodes)
G.add_edges_from(edges)

### Part 1 ###
goldGraph = G.subgraph(node_connected_component(nx.Graph(G), 'shiny gold'))
outsideGold_tree = dfs_tree(goldGraph.reverse(), source='shiny gold')  # All bags leading to (containing) gold.

print(f'There are {outsideGold_tree.number_of_nodes()-1:,} other bags in the reverse tree rooted at the '
      '`shiny gold` bag, that is bags that eventually contain a `shiny gold` bag.')

### Part 2 ###
insideGold_tree = dfs_tree(goldGraph, source='shiny gold')  # All bags contained by gold.

insideGold_nBags = sum([
    prod([G.edges[u,v]['nBags'] for u,v in path])
    for path in
    all_simple_edge_paths(goldGraph,
                            source='shiny gold',
                            target=[node for node in insideGold_tree.nodes() if node != 'shiny gold'])
    ])

print(f'Total bags inside a `shiny gold` bag is {insideGold_nBags:,}.')
