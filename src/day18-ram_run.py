import networkx as nx
from santas_little_helpers import day, get_data, timed
from santas_little_utils import neighbours, ints, all_points

today = day(2024, 18)

w = h = 70
start, end = (0, 0), (w, h)
base_points = set(all_points(w+1, h+1))


def find_shortest_exit(traversable):
  g = nx.Graph()
  for p in traversable:
    g.add_node(p)
    for n in neighbours(p, borders=traversable):
      g.add_edge(p, n)
  if nx.has_path(g, start, end):
    return nx.shortest_path_length(g, start, end)
  return None


def find_first_blocking(falling_bytes):
  last_blocking = None
  for l in reversed(range(len(falling_bytes))):
    if not find_shortest_exit(base_points - set(falling_bytes[:l + 1])):
      last_blocking = falling_bytes[l]
    else:
      return ','.join(map(str, last_blocking))


def main():
  falling_bytes = list(get_data(today, [('func', (ints, ','))], groups=False))
  print(f'{today} star 1 = {find_shortest_exit(base_points - set(falling_bytes[:1024]))}')
  print(f'{today} star 2 = {find_first_blocking(falling_bytes)}')


if __name__ == '__main__':
  timed(main)
