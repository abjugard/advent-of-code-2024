from santas_little_helpers import day, get_data, timed
from functools import cache

today = day(2024, 11)


@cache
def count_splits(stone, left=25):
  if left == 0:
    return 1

  if stone == 0:
    return count_splits(1, left-1)

  str_stone = str(stone)
  digits = len(str_stone)
  if digits % 2 == 0:
    l, r = str_stone[:digits // 2], str_stone[digits // 2:]
    return count_splits(int(l), left-1) + count_splits(int(r), left-1)

  return count_splits(stone * 2024, left-1)


def parse(line):
  return list(map(int, line.split()))


def main():
  stones = next(get_data(today, parse))
  print(f'{today} star 1 = {sum(count_splits(stone) for stone in stones)}')
  print(f'{today} star 2 = {sum(count_splits(stone, 75) for stone in stones)}')


if __name__ == '__main__':
  timed(main)
