from collections import Counter
from santas_little_helpers import day, get_data, timed
from santas_little_utils import transpose

today = day(2024, 25)


def parse(line):
  teeth = transpose(line)
  is_lock = teeth[0][0] == '#'
  configuration = [Counter(column)['#'] for column in teeth]
  return is_lock, configuration


def main():
  data = list(map(parse, get_data(today, groups=True)))
  fits = sum(
    all(lock[idx] + key[idx] <= 7 for idx in range(5))
    for is_lock, lock in data if is_lock
    for is_lock, key in data if not is_lock
  )
  print(f'{today} star 1 = {fits}')


if __name__ == '__main__':
  timed(main)
