import networkx as nx
from santas_little_helpers import day, get_data, timed
from santas_little_utils import build_dict_map, neighbours

today = day(2024, 20)


def build_graph(the_map, d, noclip=False):
  g = nx.Graph()
  start = end = None
  for p, c in the_map.items():
    if c == '#' and not noclip:
      continue
    if c == 'S':
      start = p
    if c == 'E':
      end = p
    for n in neighbours(p, borders=(d if noclip else the_map)):
      if the_map[n] == '#' and not noclip:
        continue
      g.add_edge(p, n)
  return g, start, end


def find_cheats(data, noclip_distance=2):
  g, start, end = build_graph(*data)
  g_all, *_ = build_graph(*data, noclip=True)

  time_to_beat = nx.shortest_path_length(g, start, end) - 100
  from_start = nx.shortest_path_length(g, start)
  to_end = nx.shortest_path_length(g, end)

  count = 0
  for c_s in g.nodes():
    if c_s == end:
      continue
    cheats = nx.single_source_shortest_path_length(g_all, c_s, cutoff=noclip_distance)
    for c_e, clip_length in cheats.items():
      if c_e in g.nodes():
        count += from_start[c_s] + clip_length + to_end[c_e] <= time_to_beat
  return count


def main():
  data = build_dict_map(get_data(today))
  print(f'{today} star 1 = {find_cheats(data)}')
  print(f'{today} star 2 = {find_cheats(data, noclip_distance=20)}')


if __name__ == '__main__':
  timed(main)
