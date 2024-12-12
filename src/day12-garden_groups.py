from santas_little_helpers import day, get_data, timed
from santas_little_utils import build_dict_map, neighbours
from santas_little_classes import Point, Heading

today = day(2024, 12)


def find_area(the_map, p, plant_type):
  queue = set(neighbours(p, borders=the_map))
  seen, area = {p}, {p}
  while queue:
    pn = queue.pop()
    if pn not in seen:
      seen.add(pn)
      if the_map[pn] == plant_type:
        area.add(pn)
        queue.update(set(neighbours(pn, borders=the_map)) - seen)
  return area


def find_perimeter(area):
  pp_candidates = set()
  for p in area:
    pp_candidates.update(set(neighbours(p, diagonals=True, borders=lambda pc: pc not in area)))

  perimeter, perimeter_ps = 0, set()
  for pp_cand in pp_candidates:
    ns = list(neighbours(pp_cand, borders=area))
    if any(ns):
      perimeter_ps.add(Point(*pp_cand))
      perimeter += len(ns)
    if any(set(neighbours(pp_cand, borders=area, diagonals=True, normal=False))):
      perimeter_ps.add(Point(*pp_cand))
  return perimeter, perimeter_ps


def calculate_price(the_map):
  seen, areas = set(), []
  for p, plant_type in the_map.items():
    if p not in seen:
      area = find_area(the_map, p, plant_type)
      seen.update(area)
      areas.append(area)

  cost, part2_prep = 0, []
  for area in areas:
    perimeter, perimeter_ps = find_perimeter(area)
    cost += len(area) * perimeter
    part2_prep.append((area, perimeter_ps))
  return cost, part2_prep


def find_partial_perimeters(perimeter_ps):
  seen, partials = set(), []
  for p in perimeter_ps:
    if p.t not in seen:
      seen.add(p.t)
      queue, partial = set(neighbours(p.t, borders=perimeter_ps)), {p}
      while len(queue) > 0:
        pn = queue.pop()
        seen.add(pn)
        partial.add(Point(*pn))
        queue.update(set(neighbours(pn, borders=perimeter_ps)) - seen)
      partials.append(partial)
  return partials


def find_sides(area, perimeter):
  all_sides = 0
  for partial in find_partial_perimeters(perimeter):
    if len(partial) <= 2:
      all_sides += 4
      continue

    pos, d = max(partial), Heading()
    while pos + d not in partial or all(p.t not in area for p in [pos + d + d.l, pos + d.l]):
      d.turn_l()

    target, sides, started = (pos.t, d), 0, False
    while (pos.t, d) != target or not started:
      started = True
      pos += d
      if (pos + d.l).t not in area:
        d.turn_l()
        sides += 1
      elif pos + d not in partial:
        if pos + d.r in partial:
          d.turn_r()
          sides += 1
        else:
          d.u_turn()
          sides += 2
    all_sides += sides
  return all_sides


def calculate_discounted_price(areas):
  cost = 0
  for area, perimeter in areas:
    cost += len(area) * find_sides(area, perimeter)
  return cost


def main():
  the_map, _ = build_dict_map(get_data(today))
  star1, areas = calculate_price(the_map)
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {calculate_discounted_price(areas)}')


if __name__ == '__main__':
  timed(main)
