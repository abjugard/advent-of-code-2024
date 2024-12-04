from santas_little_helpers import day, get_data, timed
from santas_little_utils import build_dict_map, neighbours

today = day(2024, 4)
MS = set('MS')


def xmas_finder(grid, keys):
  count = 0
  dirs = list(neighbours(labels=False, diagonals=True))
  for x, y in keys:
    if grid[(x, y)] != 'X':
      continue
    for dx, dy in dirs:
      count += 'M' == grid[(x+dx,   y+dy)] \
           and 'A' == grid[(x+dx*2, y+dy*2)] \
           and 'S' == grid[(x+dx*3, y+dy*3)]
  return count


def x_mas_finder(grid, keys):
  count = 0
  for x, y in keys:
    if grid[(x, y)] != 'A':
      continue
    count += MS == {grid[(x-1, y-1)], grid[(x+1, y+1)]} \
                == {grid[(x-1, y+1)], grid[(x+1, y-1)]}
  return count


def main():
  grid, _ = build_dict_map(get_data(today), default='.')
  keys = list(grid.keys())
  print(f'{today} star 1 = {xmas_finder(grid, keys)}')
  print(f'{today} star 2 = {x_mas_finder(grid, keys)}')


if __name__ == '__main__':
  timed(main)
