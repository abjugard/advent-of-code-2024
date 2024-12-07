from santas_little_helpers import day, get_data, timed

today = day(2024, 7)


def test_equations(equations, concat = False):
  def test_eqn(test_value, eqn):
    def dfs(rest):
      if len(rest) == 1:
        return test_value == rest[0]
      n1, n2, *tail = rest
      if n1 > test_value:
        return False
      if dfs([n1 * n2] + tail) or dfs([n1 + n2] + tail):
        return True
      return concat and dfs([int(f'{n1}{n2}')] + tail)
    return test_value * dfs(eqn)
  return sum(test_eqn(*eqn) for eqn in equations)


def parse(line):
  test_value, eqn = line.split(':')
  return int(test_value), list(map(int, eqn.split()))


def main():
  equations = list(get_data(today, parse))
  print(f'{today} star 1 = {test_equations(equations)}')
  print(f'{today} star 2 = {test_equations(equations, concat = True)}')


if __name__ == '__main__':
  timed(main)
