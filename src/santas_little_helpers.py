import json, re, importlib, sys, os
from time import time
from datetime import date
from pathlib import Path
from typing import Callable, Iterator
from functools import reduce
from itertools import product

setup_start = time()

alphabet = 'abcdefghijklmnopqrstuvwxyz'
ALPHABET = alphabet.upper()
full_alphabet = alphabet + ALPHABET

base_ops = [('replace', (r'\n', ''))]

aoc_root = Path(__file__).resolve().parent.parent
aoc_data = aoc_root / 'data'

with (aoc_root / 'config.json').open('r') as f:
  config = json.load(f)


def day(year: int, theday: int) -> date:
  global setup_start
  setup_start = time()
  return date(year, 12, theday)


def build_op(op, args):
  if op == 'func':
    if isinstance(args, tuple):
      return lambda line: args[0](line, *args[1])
    else:
      return lambda line: args(line)
  elif op == 'map':
    return lambda line: list(map(args, line))
  elif op == 'replace':
    matcher = re.compile(args[0])
    return lambda line: matcher.sub(args[1], line)
  elif op == 'split':
    return lambda line: line.split(args)
  elif op == 'translate':
    if isinstance(args, dict):
      translations = str.maketrans(args)
    else:
      translations = str.maketrans(*args)
    return lambda line: line.translate(translations)
  elif op == 'translatemany':
    targets, replacement = args
    translations = str.maketrans(targets, replacement * len(targets))
    return lambda line: line.translate(translations)


def build_op_chain(ops):
  for op, args in ops:
    yield build_op(op, args)


def format_line(line, op_chain):
  return reduce(lambda data, op: op(data), op_chain, line)


def import_requests():
  from requests import request, codes
  return request, codes


def get_data(today: date = date.today(), ops: list = base_ops, groups: bool = False) -> Iterator:
  if not aoc_data.exists():
    aoc_data.mkdir()

  def save_daily_input(today: date) -> None:
    request, status_codes = import_requests()
    url = f'https://adventofcode.com/{today.year}/day/{today.day}/input'
    res = request('GET', url, cookies=config)
    if res.status_code != status_codes.ok:
      print(f'Day {today.day} not available yet')
      sys.exit(0)
    with file_path.open('wb') as f:
      for chunk in res.iter_content(chunk_size=128):
        f.write(chunk)

  file_root = aoc_data / str(today.year)
  if not file_root.exists():
    file_root.mkdir()

  file_path = file_root / f'day{today.day:02}.txt'
  if not file_path.exists():
    print(f'Data for day {today.day} not available, downloading!')
    save_daily_input(today)

  op_chain = list(build_op_chain(ops))
  with file_path.open() as f:
    lines = f.read().rstrip().split('\n\n' if groups else '\n')
  if groups:
    def format_group(group_lines):
      for line in group_lines.split('\n'):
        yield format_line(line, op_chain)
    for group in lines:
      yield format_group(group)
  else:
    for line in lines:
      yield format_line(line, op_chain)


def time_fmt(delta: float) -> (float, str):
  if delta < 1e-6:
    return 1e9, 'ns'
  elif delta < 1e-3:
    return 1e6, 'µs'
  elif delta < 1:
    return 1e3, 'ms'
  return 1, 'seconds'


def execute(func: Callable) -> float:
  start = time()
  result = func()
  return result, time() - start


def execute_multiple(func: Callable, times) -> [float]:
  setup = time() - setup_start
  _, initial = execute(func)
  if times is None:
    times = 1000 if initial < 0.005 else 100
  deltas = [initial + setup]

  disable_stdout()
  for _ in range(times - 1):
    deltas += [execute(func)[1] + setup]
  restore_stdout()

  return deltas


def timed(func: Callable, start=None) -> None:
  if setup_start is not None:
    setup = time() - setup_start
  if start is not None:
    setup = time() - start
  result, delta = execute(func)
  print_result(delta + setup)
  return result


def disable_stdout() -> None:
  sys.stdout = open(os.devnull, 'w')


def restore_stdout() -> None:
  sys.stdout = sys.__stdout__


def bench(func: Callable, times=None):
  start = time()
  deltas = execute_multiple(func, times)
  total = time() - start
  times = len(deltas)
  print_result(min(deltas), 'min')
  avg = sum(deltas) / len(deltas)
  print_result(avg, 'avg')
  print_result(total, 'tot', suffix=f'(n={times})')


def average(func: Callable, times: int = 100):
  deltas = execute_multiple(func, times)
  avg = sum(deltas) / len(deltas)
  print_result(avg, 'avg')


def print_result(delta: [float], prefix: str = '', suffix: str = ''):
  multiplier, unit = time_fmt(delta)
  divider = ''
  if prefix != '':
    divider = ': '
  if suffix != '':
    suffix = ' ' + suffix
  print(f'--- {prefix}{divider}{delta*multiplier:.2f} {unit}{suffix} ---')


def run_all():
  for file in sorted(Path('.').glob('day[!X]?-*.py')):
    try:
      import_start = time()
      day = importlib.import_module(file.name[:-3])
    except Exception as e:
      print(f'Failed to import \'{file.name}\': {e}', file=sys.stderr)
      print()
      continue
    print(f'Running \'{file.name}\':')
    timed(day.main, import_start)
    print()


if __name__ == '__main__':
  timed(run_all)
