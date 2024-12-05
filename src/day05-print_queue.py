import re
from santas_little_helpers import day, get_data, timed

today = day(2024, 5)


def apply_rules(job, rules):
  js = set(job)
  passes = True
  for rule in rules:
    if not set(rule).issubset(js):
      continue
    if rule != [p for p in job if p in rule]:
      l, r = rule
      temp_job = [p for p in job if p != l]
      temp_job.insert(temp_job.index(r), l)
      job = temp_job
      passes = False
  return passes, job


def calculate_checksums(rules, jobs):
  correct = corrected = 0
  for job in jobs:
    passes, fixed = apply_rules(job, rules)
    if passes:
      correct += job[len(job) // 2]
    else:
      corrected += fixed[len(fixed) // 2]
  return correct, corrected


def parse(line):
  return list(map(int, re.split(r'\||,', line)))


def main():
  rules, jobs = get_data(today, [('func', parse)], groups=True)
  star1, star2 = calculate_checksums(sorted(rules), jobs)
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {star2}')


if __name__ == '__main__':
  timed(main)
