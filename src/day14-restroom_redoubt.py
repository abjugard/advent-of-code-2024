from santas_little_helpers import day, get_data, timed
from santas_little_utils import mul, ints
from santas_little_classes import Point
from collections import defaultdict

today = day(2024, 14)


def quadrant_bots(bots, xm, ym):
  quadrants = defaultdict(int)
  for bot, heading in bots:
    quadrants[1] += bot.x < xm and bot.y < ym
    quadrants[2] += bot.x > xm and bot.y < ym
    quadrants[3] += bot.x < xm and bot.y > ym
    quadrants[4] += bot.x > xm and bot.y > ym
  return mul(quadrants.values())


def has_some_kind_of_tree_stem_in_the_middle(ps, xm, ym):
  return all((xm, y) in ps for y in range(ym-3, ym+3))


def elapse_time(bots):
  i, xw, yw = 0, 101, 103
  xm, ym = xw // 2, yw // 2
  while True:
    c = set()
    for bot, heading in bots:
      bot.move(heading, wrap=(xw, yw))
      c.add(bot.t)
    i += 1
    if has_some_kind_of_tree_stem_in_the_middle(c, xm, ym):
      yield i
    if i == 100:
      yield quadrant_bots(bots, xm, ym)


def parse(line):
  p, v = line.split(' ')
  return (Point(*ints(p[2:], ',')),
          Point(*ints(v[2:], ',')))


def main():
  bots = list(get_data(today, parse, groups=False))
  star_gen = elapse_time(bots)
  print(f'{today} star 1 = {next(star_gen)}')
  print(f'{today} star 2 = {next(star_gen)}')


if __name__ == '__main__':
  timed(main)
