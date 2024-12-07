from santas_little_helpers import day, get_data, timed
from santas_little_classes import Point, Heading
from santas_little_utils import build_dict_map

today = day(2024, 6)


def guard_path(the_map):
  start = heading = None
  for p, c in the_map.items():
    if c in '^><v':
      start = p
      the_map[p] = '.'
      heading = Heading(c)

  p, seen = Point(*start), set()
  while True:
    seen.add((p.t, heading))
    n = p.next(heading)
    if n.t not in the_map:
      return { p for p, _ in seen }, 0
    while the_map[n.t] == '#':
      heading.turn_r()
      n = p.next(heading)
    p = n
    if (p.t, heading) in seen:
      return None, 1


def find_loops(the_map, path):
  count = 0
  for p, c in the_map.items():
    if c == '.' and p in path:
      test = the_map.copy()
      test[p] = '#'
      _, terminated = guard_path(test)
      count += terminated
  return count


def main():
  the_map, _ = build_dict_map(get_data(today))
  path, _ = guard_path(the_map.copy())
  print(f'{today} star 1 = {len(path)}')
  print(f'{today} star 2 = {find_loops(the_map, path)}')


if __name__ == '__main__':
  timed(main)
