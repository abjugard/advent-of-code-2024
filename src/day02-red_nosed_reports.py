from santas_little_helpers import day, get_data, timed
from itertools import pairwise

today = day(2024, 2)


def gradual(levels):
  return all(1 <= abs(r-l) <= 3 for l, r in pairwise(levels))


def unidirectional(levels):
  sorted_levels = sorted(levels)
  return levels == sorted_levels or levels[::-1] == sorted_levels


def safe(levels, use_problem_dampener=False):
  if unidirectional(levels) and gradual(levels):
    return True
  if not use_problem_dampener:
    return False
  for i in range(len(levels)):
    if safe(levels[:i] + levels[i+1:]):
      return True
  return False


def parse(line):
  return list(map(int, line.split()))


def main():
  reports = list(get_data(today, parse))
  print(f'{today} star 1 = {sum(safe(report) for report in reports)}')
  print(f'{today} star 2 = {sum(safe(report, use_problem_dampener=True) for report in reports)}')


if __name__ == '__main__':
  timed(main)
