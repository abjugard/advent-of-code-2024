from santas_little_helpers import day, get_data, timed

today = day(2024, 7)


def test_eqn(test_value, ns, concat = False):
  if len(ns) == 1:
    return test_value == ns[0]
  l, r, *rest = ns
  if test_eqn(test_value, [l + r] + rest, concat):
    return test_value
  if test_eqn(test_value, [l * r] + rest, concat):
    return test_value
  if concat:
    head = int(str(l) + str(r))
    if test_eqn(test_value, [head] + rest, concat):
      return test_value
  return 0


def parse(line):
  l, raw = line.split(':')
  r = raw.split()
  return int(l.strip()), list(map(int, r))


def main():
  equations = list(get_data(today, [('func', parse)]))
  print(f'{today} star 1 = {sum(test_eqn(*eqn) for eqn in equations)}')
  print(f'{today} star 2 = {sum(test_eqn(*eqn, concat=True) for eqn in equations)}')


if __name__ == '__main__':
  timed(main)
