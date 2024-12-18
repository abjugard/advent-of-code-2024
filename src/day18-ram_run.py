import networkx as nx
from santas_little_helpers import day, get_data, timed
from santas_little_utils import neighbours, ints, all_points

today = day(2024, 18)


def find_shortest_exit(traversable):
  g = nx.Graph()
  for p in traversable:
    g.add_node(p)
    for n in neighbours(p, borders=traversable):
      g.add_edge(p, n)
  if nx.has_path(g, (0, 0), (70, 70)):
    return set(nx.shortest_path(g, (0, 0), (70, 70)))
  return None


def find_first_blocking(traversable, falling_bytes):
  last_blocking = None
  while path := find_shortest_exit(traversable):
    while falling_bytes:
      last_blocking = falling_bytes.pop(0)
      traversable.remove(last_blocking)
      if last_blocking in path:
        break
  return ','.join(map(str, last_blocking))


def main():
  falling_bytes = list(get_data(today, [('func', (ints, ','))], groups=False))
  fallen, falling = falling_bytes[:1024], falling_bytes[1024:]
  base_points = set(all_points(71, 71)) - set(fallen)
  print(f'{today} star 1 = {len(find_shortest_exit(base_points))-1}')
  print(f'{today} star 2 = {find_first_blocking(base_points, falling)}')


if __name__ == '__main__':
  timed(main)
