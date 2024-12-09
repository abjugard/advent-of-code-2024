from santas_little_helpers import day, get_data, timed

today = day(2024, 9)


def compress(filesystem):
  filesystem_blocks = dict()
  block_index = 0
  for entry in filesystem:
    k = entry[0]
    if k == 'file':
      _, size, file_id = entry
      for i in range(size):
        filesystem_blocks[block_index + i] = file_id
      block_index += size
    else:
      free_blocks = entry[1]
      for i in range(free_blocks):
        filesystem_blocks[block_index + i] = None
      block_index += free_blocks
  data = list(reversed(filesystem_blocks.items()))
  new_fs = dict()
  moved = 0
  disk_size = max(filesystem_blocks.keys())
  for bi, c in filesystem_blocks.items():
    if bi > disk_size-moved:
      break
    if c is None:
      file_id = None
      while file_id is None:
        bi_data, file_id = data.pop(0)
        filesystem_blocks[bi_data] = 0
        moved += 1
        if bi_data == bi:
          break
      new_fs[bi] = file_id or 0
    else:
      new_fs[bi] = filesystem_blocks[bi]
  checksum = 0
  for bi, file_id in new_fs.items():
    checksum += bi*file_id
  return checksum


def merge_free_space(filesystem):
  new_fs = []
  free_space = 0
  for i in range(len(filesystem)):
    k, s, v = filesystem[i]
    if k == 'file':
      new_fs.append((k, s, v))
      free_space = 0
      continue
    free_space += s
    if i + 1 < len(filesystem):
      k, s, v = filesystem[i+1]
      if k == 'space':
        continue
    new_fs.append(('space', free_space, 0))
  return new_fs



def move_one(filesystem, file):
  moved = False
  new_fs = list()
  for entry in filesystem:
    if moved:
      if entry != file:
        new_fs.append(entry)
      else:
        new_fs.append(('space', entry[1], 0))
      continue
    k = entry[0]
    if k == 'file':
      if entry == file:
        moved = True
      new_fs.append(entry)
      continue
    free_space = entry[1]
    _, size, file_id = file
    if free_space < size:
      new_fs.append(entry)
      continue
    new_fs.append(('file', size, file_id))
    moved = True
    free_space -= size
    if free_space > 0:
      new_fs.append(('space', free_space, 0))
  return merge_free_space(new_fs), moved


def compress2(filesystem):
  files = [entry for entry in filesystem[::-1] if entry[0] == 'file']
  for file in files:
    filesystem, _ = move_one(filesystem, file)
  bi = checksum = 0
  for _, n, v in filesystem:
    for _ in range(n):
      checksum += bi*v
      bi += 1
  return checksum


def parse(raw):
  file_id = 0
  filesystem = []
  for i in range(0, len(raw), 2):
    size = int(raw[i])

    filesystem.append(('file', size, file_id))

    if (i+1) >= len(raw):
      break
    free_space = int(raw[i+1])
    filesystem.append(('space', free_space, 0))

    file_id += 1
  return filesystem


def main():
  inp = next(get_data(today))
  filesystem = parse(inp)
  print(f'{today} star 1 = {compress(filesystem)}')
  print(f'{today} star 2 = {compress2(filesystem)}')


if __name__ == '__main__':
  timed(main)
