from santas_little_helpers import day, get_data, timed

today = day(2024, 9)


def compress_blocks(filesystem):
  block_index, filesystem_blocks = 0, dict()
  for k, size, file_idx in filesystem:
    for i in range(size):
      filesystem_blocks[block_index + i] = file_idx
    block_index += size

  files = list(filesystem_blocks.items())
  new_fs, moved, disk_size = dict(), 0, block_index
  for bi, bv in filesystem_blocks.items():
    if bi >= disk_size-moved:
      break
    if bv is not None:
      new_fs[bi] = bv
    else:
      file_idx = None
      while file_idx is None:
        bi_file, file_idx = files.pop()
        moved += 1
        if bi_file <= bi:
          break
      new_fs[bi] = file_idx

  return sum(bi*(file_idx or 0) for bi, file_idx in new_fs.items())


def move(filesystem, target_id, target_size):
  done, new_fs = False, []
  for entry in filesystem:
    k, size, idx = entry
    if done:
      new_fs.append(entry if idx != target_id else ('space', size, 0))
      continue
    if k == 'file' or size < target_size:
      if idx == target_id:
        done = True
      new_fs.append(entry)
      continue
    new_fs.append(('file', target_size, target_id))
    done = True
    size -= target_size
    if size > 0:
      new_fs.append(('space', size, 0))
  return new_fs


def simplify(filesystem, files):
  smallest = min(size for _, size in files)
  for locked_idx, (k, size, file_idx) in enumerate(filesystem):
    if k == 'space' and size >= smallest:
      return filesystem[:locked_idx], filesystem[locked_idx:]


def compress_files(filesystem):
  files = [(idx, size) for k, size, idx in filesystem[::-1] if k == 'file']
  seen, locked = set(), []
  for idx, file in enumerate(files):
    if file[0] in seen:
      continue
    filesystem = move(filesystem, *file)
    done, filesystem = simplify(filesystem, files[idx:])
    seen.update(file_idx for _, _, file_idx in done)
    locked += done

  bi = checksum = 0
  for _, n, file_idx in locked + filesystem:
    for _ in range(n):
      checksum += bi*(file_idx or 0)
      bi += 1
  return checksum


def parse(disk):
  file_id, filesystem = 0, []
  for i in range(0, len(disk), 2):
    size = int(disk[i])
    filesystem.append(('file', size, file_id))
    if (i+1) >= len(disk):
      break
    free_space = int(disk[i + 1])
    filesystem.append(('space', free_space, None))
    file_id += 1
  return filesystem


def main():
  filesystem = next(get_data(today, parse))
  print(f'{today} star 1 = {compress_blocks(filesystem)}')
  print(f'{today} star 2 = {compress_files(filesystem)}')


if __name__ == '__main__':
  timed(main)
