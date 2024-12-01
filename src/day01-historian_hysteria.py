from santas_little_helpers import day, get_data, timed
from collections import Counter

today = day(2024, 1)


def part1(left, right):
  return sum(abs(r-l) for l, r in zip(sorted(left), sorted(right)))


def part2(left, right):
  lookup = Counter(right)
  return sum(n*lookup[n] for n in left)


def parse(line):
  l, r = line.split()
  return int(l), int(r)


def main():
  location_id_lists = list(zip(*get_data(today, [('func', parse)])))
  print(f'{today} star 1 = {part1(*location_id_lists)}')
  print(f'{today} star 2 = {part2(*location_id_lists)}')


if __name__ == '__main__':
  timed(main)
