from functools import cache
from santas_little_helpers import day, get_data, timed

today = day(2024, 19)


towels = []


@cache
def is_possible(pattern):
  if len(pattern) == 0:
    return True
  return any(
    is_possible(pattern[len(towel):])
    for towel in towels
    if pattern.startswith(towel)
  )


@cache
def count_ways(pattern):
  if len(pattern) == 0:
    return 1
  return sum(
    count_ways(pattern[len(towel):])
    for towel in towels
    if pattern.startswith(towel)
  )


def main():
  global towels
  towels, patterns = list(get_data(today, groups=True))
  patterns = list(patterns)
  towels = list(next(towels).split(', '))
  print(f'{today} star 1 = {sum(is_possible(p) for p in patterns)}')
  print(f'{today} star 2 = {sum(count_ways(p) for p in patterns)}')


if __name__ == '__main__':
  timed(main)
