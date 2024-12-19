from functools import cache
from santas_little_helpers import day, get_data, timed

today = day(2024, 19)
towels = []


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
  towels_raw, patterns = get_data(today, groups=True)
  towels.extend(next(towels_raw).split(', '))

  ways = list(filter(None, (count_ways(pattern) for pattern in patterns)))
  print(f'{today} star 1 = {len(ways)}')
  print(f'{today} star 2 = {sum(ways)}')


if __name__ == '__main__':
  timed(main)
