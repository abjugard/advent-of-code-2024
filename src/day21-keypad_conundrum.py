from collections import defaultdict, Counter
from santas_little_classes import Point
from santas_little_helpers import day, get_data, timed

today = day(2024, 21)

def make_pad(pad_keys):
  return {
    key: Point(x, y)
    for y, ks in enumerate(pad_keys)
    for x, key in enumerate(ks)
  }

numpad = make_pad(['789', '456', '123', '.0A'])
dirpad = make_pad(['.^A', '<v>'])


def generic_mover(d):
  sequence = ''
  if d.x < 0:
    sequence += '<' * -d.x
  v_char = '^' if d.y < 0 else 'v'
  sequence += v_char * abs(d.y)
  if d.x > 0:
    sequence += '>' * d.x
  return sequence


def dirpad_mover(sequence):    #     +---+---+
  p = dirpad['A']              #     | ^ | A |
  for c in sequence:           # +---+---+---+
    target = dirpad[c]         # | < | v | > |
    d = target - p             # +---+---+---+

    if   p == dirpad['<'] and d.y < 0:
      yield '>' * d.x + '^'
    elif p == dirpad['^'] and d == (-1, 1):
      yield 'v<'
    elif p == dirpad['A'] and d == (-2, 1):
      yield 'v<<'
    else:
      yield generic_mover(d)   # +---+---+---+
    p = target                 # | 7 | 8 | 9 |
                               # +---+---+---+
                               # | 4 | 5 | 6 |
def numpad_mover(sequence):    # +---+---+---+
  p = numpad['A']              # | 1 | 2 | 3 |
  for c in sequence:           # +---+---+---+
    target = numpad[c]         #     | 0 | A |
    d = target - p             #     +---+---+

    if   p == numpad['A'] and d.x == -2:
      yield '^' * -d.y + '<<'
    elif p == numpad['0'] and d.x == -1:
      yield '^' * -d.y + '<'
    else:
      yield generic_mover(d)
    p = target


def expand_sequences(sequences, move_func):
  new_sequences = defaultdict(int)
  for seq, orig_count in sequences.items():
    for n_seq, count in Counter(move_func(seq)).items():
      new_sequences[n_seq + 'A'] += count * orig_count
  return new_sequences


def handle_code(code, bots):
  sequences = expand_sequences({code: 1}, numpad_mover)
  for i in range(1, max(bots) + 1):
    sequences = expand_sequences(sequences, dirpad_mover)
    if i in bots:
      yield sum(len(seq) * n for seq, n in sequences.items()) * int(code[:-1])


def find_complexities(data, bots):
  c = Point()
  for code in data:
    c += tuple(handle_code(code, bots))
  return c.t


def main():
  star1, star2 = find_complexities(get_data(today, groups=False), bots=[2, 25])
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {star2}')


if __name__ == '__main__':
  timed(main)
