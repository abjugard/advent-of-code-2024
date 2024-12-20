import networkx as nx
from santas_little_helpers import day, get_data, timed
from santas_little_utils import build_dict_map, neighbours

today = day(2024, 20)


def build_graph(the_map, d, noclip=False):
  g = nx.Graph()
  start = end = None
  for p, c in the_map.items():
    if c == 'S': start = p
    if c == 'E': end = p
    if c != '#' or noclip:
      for n in neighbours(p, borders=(d if noclip else the_map)):
        if the_map[n] != '#' or noclip:
          g.add_edge(p, n)
  return g, start, end


def find_cheats(data, noclip_distance=2):
  g, start, end = build_graph(*data)
  g_all, *_ = build_graph(*data, noclip=True)

  time_to_beat = nx.shortest_path_length(g, start, end) - 100
  from_start   = nx.shortest_path_length(g, start)
  to_end       = nx.shortest_path_length(g, end)

  count = 0
  for c_start in g.nodes():
    cheats = nx.single_source_shortest_path_length(g_all, c_start, cutoff=noclip_distance)
    for c_end, clip_length in cheats.items():
      if c_end in g.nodes():
        count += from_start[c_start] + clip_length + to_end[c_end] <= time_to_beat
  return count


def main():
  data = build_dict_map(get_data(today))
  print(f'{today} star 1 = {find_cheats(data)}')
  print(f'{today} star 2 = {find_cheats(data, noclip_distance=20)}')


if __name__ == '__main__':
  timed(main)
