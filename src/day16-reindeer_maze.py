import networkx as nx
from santas_little_helpers import day, get_data, timed
from santas_little_utils import build_dict_map, turn
from santas_little_classes import Point

today = day(2024, 16)


def build_graph(the_map):
  start = end = None
  g = nx.DiGraph()

  for p, c in the_map.items():
    if c == '#':
      continue
    p = Point(*p)
    for d in 'NEWS':
      g.add_node((p, d))

    if c == 'S':
      start = (p, 'E')
    if c == 'E':
      end = p

  for p, d in g.nodes:
    if (p.next(d), d) in g.nodes:
      g.add_edge((p, d), (p.next(d), d), weight=1)

    t = turn[d]
    g.add_edge((p, d), (p, t.l), weight=1000)
    g.add_edge((p, d), (p, t.r), weight=1000)

  for d in 'NEWS':
    g.add_edge((end, d), 'target', weight=0)

  return g, start


def places_to_sit(g, start):
  ps = set()
  for path in nx.all_shortest_paths(g, start, 'target', weight='weight'):
    for node, _ in path[:-1]:
      ps.add(node.t)

  return len(ps)


def main():
  the_map, _ = build_dict_map(get_data(today))
  g, start = build_graph(the_map)
  print(f'{today} star 1 = {nx.shortest_path_length(g, start, 'target', weight='weight')}')
  print(f'{today} star 2 = {places_to_sit(g, start)}')


if __name__ == '__main__':
  timed(main)
