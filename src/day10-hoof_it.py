from santas_little_helpers import day, get_data, timed
from santas_little_utils import build_dict_map, neighbours
from collections import defaultdict
import networkx as nx

today = day(2024, 10)


def score_trailheads(g, trailheads, goals):
  scores, distinct = defaultdict(int), defaultdict(int)
  for start in trailheads:
    for goal in goals:
      path_count = len(list(nx.all_simple_paths(g, start, goal)))
      scores[start] += path_count > 0
      distinct[start] += path_count
  return sum(scores.values()), sum(distinct.values())


def build_graph(inp):
  the_map, _ = build_dict_map(inp, conv_func=lambda c, _: int(c))
  trailheads, goals = [], []

  g = nx.DiGraph()
  for p, c in the_map.items():
    g.add_node(p)
    for n in neighbours(p, borders=the_map):
      if the_map[n] == c + 1:
        g.add_edge(p, n)
    if c == 0:
      trailheads.append(p)
    if c == 9:
      goals.append(p)
  return g, trailheads, goals


def main():
  inp = build_graph(get_data(today))
  star1, star2 = score_trailheads(*inp)
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {star2}')


if __name__ == '__main__':
  timed(main)
