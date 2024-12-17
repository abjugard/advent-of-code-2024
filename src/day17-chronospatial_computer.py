from santas_little_helpers import day, get_data, timed
from santas_little_utils import ints

today = day(2024, 17)


def get_combo(operand, a, b, c):
  if   operand == 4: return a
  elif operand == 5: return b
  elif operand == 6: return c
  return operand


def run_vm(a, program):
  pc = b = c = 0
  out = []
  while pc < len(program)-1:
    instr = program[pc]
    operand = program[pc+1]
    inc = True

    if   instr == 0: # adv
      a //= pow(2, get_combo(operand, a, b, c))
    elif instr == 1: # bxl
      b ^= operand
    elif instr == 2: # bst
      b = get_combo(operand, a, b, c) % 8
    elif instr == 3: # jnz
      if a != 0:
        inc = False
        pc = operand
    elif instr == 4: # bxc
      b ^= c
    elif instr == 5: # out
      out.append(get_combo(operand, a, b, c) % 8)
    elif instr == 6: # bdv
      b = a // pow(2, get_combo(operand, a, b, c))
    elif instr == 7: # cdv
      c = a // pow(2, get_combo(operand, a, b, c))
    if inc:
      pc += 2
  return out


def find_quine(program):
  a = pow(8, len(program)-1)
  while (out := run_vm(a, program)) != program:
    for idx, o in reversed(list(enumerate(out))):
      if o != program[idx]:
        a += 8**idx
        break
  return a


def main():
  registers, program = get_data(today, [('split', ': '), ('skip', 1), ('elem', 0)], groups=True)
  register_a = int(next(registers))
  program = list(ints(next(program), ','))

  print(f'{today} star 1 = {",".join(map(str, run_vm(register_a, program)))}')
  print(f'{today} star 2 = {find_quine(program)}')


if __name__ == '__main__':
  timed(main)
