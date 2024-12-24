import re
from santas_little_helpers import day, get_data, timed

today = day(2024, 24)

wire_re = re.compile(r'(\w{3}) (\w+) (\w{3}) -> (\w{3})')


def compute_out(l, r, op):
  if op == 'OR':    return l or r
  elif op == 'AND': return l and r
  elif op == 'XOR': return l ^ r


def run_adder(inputs, wires):
  last, curr = None, len(inputs)
  while curr != last:
    last = curr
    for l, r, op, out in wires:
      if l in inputs and r in inputs and out not in inputs:
        inputs[out] = compute_out(inputs[l], inputs[r], op)
    curr = len(inputs)

  bits = ''
  for out, val in sorted(inputs.items(), reverse=True):
    if out.startswith('z'):
      bits += f'{int(val)}'
  return int(bits, 2)


def repair_adder(wires):
  curr, idx, swaps = None, 0, SwapDict()
  def find_output(l, r, op):
    lookup = {swaps[l], swaps[r]}
    for l, r, sub_op, out in wires:
      lr = {swaps[l], swaps[r]}
      if lr == lookup and sub_op == op:
        return swaps[out]

  while idx < 45:
    x_wire, y_wire, z_wire = [f'{c}{idx:02d}' for c in 'xyz']
    if idx == 0:
      curr = find_output(x_wire, y_wire, 'AND')
    else:
      xor_out = find_output(x_wire, y_wire, 'XOR')
      and_out = find_output(x_wire, y_wire, 'AND')

      carry_xor_out = find_output(xor_out, curr, 'XOR')
      if carry_xor_out == z_wire:
        carry_and_out = find_output(xor_out, curr, 'AND')
        curr = find_output(and_out, carry_and_out, 'OR')
      else:
        if carry_xor_out is not None:
          swaps[carry_xor_out] = z_wire
        else:
          swaps[xor_out] = and_out
        idx = 0
        continue
    idx += 1

  return ",".join(sorted(swaps.keys()))


def parse_wire(wire):
  l, op, r, out = re.match(wire_re, wire).groups()
  return l, r, op, out


def main():
  data = get_data(today, groups=True)
  inputs = [inp.split(': ') for inp in next(data)]
  inputs = {label: int(value) for label, value in inputs}
  wires = list(map(parse_wire, next(data)))

  print(f'{today} star 1 = {run_adder(inputs, wires)}')
  print(f'{today} star 2 = {repair_adder(wires)}')


class SwapDict(dict):
  def __setitem__(self, key, value):
    dict.__setitem__(self, key, value)
    dict.__setitem__(self, value, key)

  def __delitem__(self, key):
    dict.__delitem__(self, self[key])
    dict.__delitem__(self, key)

  def __getitem__(self, key):
    return dict.__getitem__(self, key) if key in self else key


if __name__ == '__main__':
  timed(main)
