import re
from santas_little_helpers import day, get_data, timed

today = day(2024, 3)
scan_re = r"(mul\((\d+),(\d+)\)|do\(\)|don't\(\))"


def scan(data, always_active=True):
  count, active = 0, True
  for match in re.finditer(scan_re, data, re.MULTILINE):
    instr = match.groups()[0]
    if instr.startswith('do'):
      active = instr == 'do()'
      continue
    if active or always_active:
      _, l, r = match.groups()
      count += int(l) * int(r)
  return count


def main():
  memory = ''.join(get_data(today))
  print(f'{today} star 1 = {scan(memory)}')
  print(f'{today} star 2 = {scan(memory, always_active=False)}')


if __name__ == '__main__':
  timed(main)
