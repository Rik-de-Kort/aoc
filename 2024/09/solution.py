from copy import deepcopy
from pathlib import Path

folder = Path(__file__).parent

with open(folder / 'input.txt') as handle:
    data = [int(c) for c in handle.read().strip()]
disk = []
id_number = 0
for i, x in enumerate(data):
    if i % 2 == 0:  # file
        disk.extend([id_number] * x)
        id_number += 1
    else:  # Free space
        disk.extend([-1] * x)  # free space
raw_disk = deepcopy(disk)


def display(disk):
    print(''.join((str(i) if i >= 0 else '.' for i in disk)))


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


def files_and_frees(disk):
    files = []
    i = 0
    while i < len(disk):
        i0 = i
        while i < len(disk) and disk[i] == disk[i0]:
            i += 1
        files.append((i0, i - i0))

    free_spaces = [(start, size) for start, size in files if disk[start] == -1]
    files = [(start, size) for start, size in files if disk[start] != -1]
    return files, free_spaces


def move(file, i, disk):
    start, size = file
    assert disk[i:i + size] == [-1] * size, disk[i:i+size]
    disk[i:i + size] = disk[start:start + size]
    disk[start:start + size] = [-1] * size
    return disk


assert move((3, 2), 0, [-1, -1, -1, 1, 1, 2, 2]) == [1, 1, -1, -1, -1, 2, 2]

disk = raw_disk
files, free_spaces = files_and_frees(disk)
while files:
    print(len(files))
    i_file, s_file = files.pop()
    _, free_spaces = files_and_frees(disk)
    for (i_free, s_free) in free_spaces:
        if i_free < i_file and s_file <= s_free:
            disk = move((i_file, s_file), i_free, disk)
            break

print(sum(i*x for i, x in enumerate(disk) if x != -1))