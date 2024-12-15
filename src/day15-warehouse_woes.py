from santas_little_helpers import day, get_data, timed
from santas_little_utils import build_dict_map
from santas_little_classes import Point, Heading

today = day(2024, 15)


def shift_moved_boxes(the_map, tiles_to_move, heading):
  new_ps = set()
  for ip, item in tiles_to_move:
    the_map[ip] = '.'
    new_ps.add((ip.next(heading), item))
  for p, item in new_ps:
    the_map[p] = item


def move_simple(the_map, bot, heading, box_chars='O'):
  step = np = bot.next(heading)
  tiles_to_move = []
  while the_map[np.t] in box_chars:
    tiles_to_move.append((np, the_map[np.t]))
    np += heading
    if the_map[np.t] == '#':
      return the_map, bot

  shift_moved_boxes(the_map, tiles_to_move, heading)
  return the_map, step


def move_advanced(the_map, bot, heading):
  if heading.direction in 'EW':
    return move_simple(the_map, bot, heading, box_chars='[]')

  step = np = bot.next(heading)
  tiles_to_move, to_check = set(), {np}
  while True:
    for p in list(to_check):
      c = the_map[p.t]
      if   c == '[': to_check.add(p.e)
      elif c == ']': to_check.add(p.w)
      elif c == '.': to_check.remove(p)
      elif c == '#':
        return the_map, bot
    tiles_to_move.update((p, the_map[p.t]) for p in to_check)
    to_check = set(p.next(heading) for p in to_check)
    if all(the_map[p] == '.' for p in to_check):
      break

  shift_moved_boxes(the_map, tiles_to_move, heading)
  return the_map, step


def play_sokoban(the_map, instructions, move_func=move_simple):
  the_map, _ = build_dict_map(the_map)
  bot = None
  for p, c in the_map.items():
    if c == '@':
      bot = Point(*p)
      the_map[p] = '.'

  for heading in instructions:
    step = bot.next(heading)
    nt = the_map[step.t]
    if nt in '.':
      bot = step
    elif nt != '#':
      the_map, bot = move_func(the_map, bot, heading)

  return sum(100*y + x for (x, y), c in the_map.items() if c in '[O')


def expand(orig_map):
  for line in orig_map:
    new_line = ''
    for c in line:
      if   c == '#': new_line += '##'
      elif c == '@': new_line += '@.'
      elif c == 'O': new_line += '[]'
      elif c == '.': new_line += '..'
    yield new_line


def main():
  the_map, instructions = list(get_data(today, groups=True))
  the_map = list(the_map)
  instructions = [Heading(c) for c in ''.join(instructions)]
  print(f'{today} star 1 = {play_sokoban(the_map, instructions)}')
  print(f'{today} star 2 = {play_sokoban(expand(the_map), instructions, move_func=move_advanced)}')


if __name__ == '__main__':
  timed(main)
