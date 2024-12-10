from santas_little_helpers import day, get_data, timed
from santas_little_utils import build_dict_map
from santas_little_classes import Point
from itertools import product

today = day(2024, 8)


def locate_antinodes(the_map):
  d, d_cand, part1_loc, part2_loc = dict(), dict(), set(), set()
  for p, c in the_map.items():
    if c != '.':
      if c not in d:
        d[c] = set()
        d_cand[c] = set(the_map.keys())
      d[c].add(Point(*p))
      d_cand[c].remove(p)

  for c, ps in d.items():
    part2_loc.update(ps)
    cand = d_cand[c]
    for p1, p2 in product(ps, repeat=2):
      offset = p2.offset_from(p1)

      p1 -= offset
      if p1.t in cand:
        part1_loc.add(p1)
      while (p1 := p1-offset).t in cand:
        part2_loc.add(p1)

      p2 += offset
      if p2.t in cand:
        part1_loc.add(p2)
      while (p2 := p2+offset).t in cand:
        part2_loc.add(p2)

  return len(part1_loc), len(part1_loc | part2_loc)


def main():
  the_map, _ = build_dict_map(get_data(today))
  star1, star2 = locate_antinodes(the_map)
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {star2}')


if __name__ == '__main__':
  timed(main)
