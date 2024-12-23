import networkx as nx
from santas_little_helpers import day, get_data, timed

today = day(2024, 23)


def solve(g):
  interconnected, lan_party = 0, []
  for clique in nx.enumerate_all_cliques(g):
    clique_length = len(clique)
    if clique_length == 3 and any(node.startswith('t') for node in clique):
      interconnected += 1
    if clique_length >= len(lan_party):
      lan_party = clique
  return interconnected, ','.join(sorted(lan_party))


def main():
  g = nx.Graph()
  for l, r in get_data(today, [('split', '-')]):
    g.add_edge(l, r)
  star1, star2 = solve(g)
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {star2}')


if __name__ == '__main__':
  timed(main)
