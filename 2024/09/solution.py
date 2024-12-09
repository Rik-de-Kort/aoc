from pathlib import Path

folder = Path(__file__).parent

with open(folder / 'input.txt') as handle:
    data = [int(c) for c in handle.read().strip()]


def display(disk):
    print(''.join((str(i) if i >= 0 else '.' for i in disk)))


disk = []
id_number = 0
for i, x in enumerate(data):
    if i % 2 == 0:  # file
        disk.extend([id_number] * x)
        id_number += 1
    else:  # Free space
        disk.extend([-1] * x)  # free space

# display(disk)

i = len(disk)
i_free = disk.index(-1)
while (i := i - 1) > i_free:
    # display(disk)
    if disk[i] == -1: continue

    disk[i_free] = disk[i]
    disk[i] = -1

    while disk[i_free] != -1 and i_free < len(disk):
        i_free += 1

# display(disk)
print(sum(i * x for i, x in enumerate(disk) if x != -1))

files = []
frees = []
id_number = 0
i_disk = 0
for i, x in enumerate(data):
    if i % 2 == 0:
        files.append((i_disk, x, id_number))
        id_number += 1
    else:
        if x == 0:
            continue
        frees.append((i_disk, x))
    i_disk += x


def display(files):
    parts = []
    for pos, size, id_number in sorted(files):
        len_current = sum(len(part) for part in parts)
        if pos > len_current:
            parts.append('.' * (pos - len_current))
        parts.append(str(id_number) * size)
    print(''.join(parts))


def is_ok(files, frees):
    combined = sorted(files + [(pos, size, -1) for pos, size in frees])
    for (pos0, size0, id0), (pos1, size1, id1) in zip(combined[:-1], combined[1:]):
        if pos0 == pos1 or pos0 + size0 > pos1:
            print(f'Overlap for {(pos0, size0, id0)} on {(pos1, size1, id1)}')
            return False
    return True


def defrag(frees):
    first, *frees = sorted(frees)
    result = [first]
    for pos, size in frees:
        last_pos, last_size = result[-1]
        if last_pos + last_size > pos:
            raise ValueError(f'Overlap {result[-1]=}, {pos=}, {size=}')
        elif last_pos + last_size == pos:
            result[-1] = last_pos, last_size + size
        else:
            result.append((pos, size))
    return result


assert is_ok(files, frees)

for i_file in range(len(files) - 1, 0, -1):
    # display(files)
    frees = defrag(frees)
    pos_file, size_file, id_number = files[i_file]
    if size_file == 0: continue
    print(f'trying to move {id_number=}')
    # assert is_ok(files, frees)
    for i_free, (pos_free, size_free) in enumerate(frees):
        if size_file <= size_free and pos_free < pos_file:
            files[i_file] = pos_free, size_file, id_number
            frees[i_free] = pos_free + size_file, size_free - size_file
            frees.append((pos_file, size_file))
            break
        elif size_free == size_file:
            files[i_file] = pos_free, size_file, id_number
            frees.pop(i_free)
            break

print(sum(sum((position + i) * id_number for i in range(size)) for position, size, id_number in sorted(files)))
