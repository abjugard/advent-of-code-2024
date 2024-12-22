from collections import defaultdict
from itertools import pairwise
from santas_little_helpers import day, get_data, timed

today = day(2024, 22)


def evolve(secret):
  secret ^= secret * 64
  secret %= 16777216
  secret ^= secret // 32
  secret %= 16777216
  secret ^= secret * 2048
  return secret % 16777216


def predict_secrets(secrets):
  count, market_data = 0, []
  for secret in secrets:
    prices = [secret % 10]
    for _ in range(2000):
      secret = evolve(secret)
      prices.append(secret % 10)
    count += secret
    market_data.append(prices)
  return count, market_data


def predict_market(market_data):
  bananas = defaultdict(int)
  for prices in market_data:
    price_changes = [p2-p1 for p1, p2 in pairwise(prices)]
    seen = set()
    for idx in range(4, len(prices)):
      sequence = tuple(price_changes[idx-4:idx])
      if sequence not in seen:
        seen.add(sequence)
        bananas[sequence] += prices[idx]
  return max(bananas.values())


def main():
  star1, market_data = predict_secrets(get_data(today, int))
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {predict_market(market_data)}')


if __name__ == '__main__':
  timed(main)
