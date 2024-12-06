from santas_little_helpers import day, get_data, timed
from santas_little_classes import Point
from santas_little_utils import build_dict_map, direction_arrow_lookup, turn

today = day(2024, 6)


def guard_path(the_map):
  start = direction = None
  for p, c in the_map.items():
    if c in '^><v':
      start = p
      the_map[p] = '.'
      direction = direction_arrow_lookup[c]

  p = Point(*start)
  seen, visited = set(), set()
  terminated = False

  while True:
    seen.add((p.t, direction))
    visited.add(p.t)
    n = p.next(direction)
    if n.t not in the_map or terminated:
      return len(visited), visited, terminated
    while the_map[n.t] == '#':
      direction = turn[direction].r
      n = p.next(direction)
    p = n
    terminated = (p.t, direction) in seen


def find_loops(the_map, path):
  count = 0
  for p, c in the_map.items():
    if c == '.' and p in path:
      test = the_map.copy()
      test[p] = '#'
      _, _, terminated = guard_path(test)
      count += terminated
  return count


def main():
  the_map, _ = build_dict_map(get_data(today))
  star1, path, _ = guard_path(the_map.copy())
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {find_loops(the_map, path)}')


if __name__ == '__main__':
  timed(main)
