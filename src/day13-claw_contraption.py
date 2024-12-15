from santas_little_helpers import day, get_data, timed
from sympy import solve, symbols, Integer

today = day(2024, 13)


def win_machine(a_inp, b_inp, prize, inc_prize=0):
  (ax, ay), (bx, by), (px, py) = a_inp, b_inp, prize

  a, b = symbols('a b')
  a, b = result = solve([
    ax*a + bx*b - px - inc_prize,
    ay*a + by*b - py - inc_prize
  ]).values()

  return 3*a + b if all(isinstance(n, Integer) for n in result) else 0


def parse(group):
  def parse_line(line):
    _, line = line.split(': ')
    l, r = line.split(', ')
    return int(l[2:]), int(r[2:])
  return list(map(parse_line, group))


def main():
  machines = list(map(parse, get_data(today, groups=True)))
  print(f'{today} star 1 = {sum(win_machine(*m) for m in machines)}')
  print(f'{today} star 2 = {sum(win_machine(*m, inc_prize=int(1e13)) for m in machines)}')


if __name__ == '__main__':
  timed(main)
