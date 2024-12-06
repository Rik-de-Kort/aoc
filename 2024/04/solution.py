import copy
from pathlib import Path
import re

folder = Path(__file__).parent

with open(folder / 'input.txt') as handle:
    data = [list(line.strip()) for line in handle.readlines()]

i_max = len(data)
j_max = len(data[0])

count = 0
# Check horizontal
for i in range(i_max):
    for j in range(j_max - 3):
        chars = [data[i][j + k] for k in range(4)]
        count += ''.join(chars) == 'XMAS' or ''.join(chars) == 'SAMX'
# Check vertical
for i in range(i_max - 3):
    for j in range(j_max):
        chars = [data[i + k][j] for k in range(4)]
        count += ''.join(chars) == 'XMAS' or ''.join(chars) == 'SAMX'
# Check diagonal top left to bottom right
for i in range(i_max - 3):
    for j in range(j_max - 3):
        chars = [data[i + k][j + k] for k in range(4)]
        count += ''.join(chars) == 'XMAS' or ''.join(chars) == 'SAMX'
# Check diagonal top right to bottom left
for i in range(i_max - 3):
    for j in range(3, j_max):
        chars = [data[i + k][j - k] for k in range(4)]
        count += ''.join(chars) == 'XMAS' or ''.join(chars) == 'SAMX'
print(count)


def print_all(items):
    print('\n'.join(''.join(line) for line in items))


count = 0
for i in range(1, i_max - 1):
    for j in range(1, j_max - 1):
        if data[i][j] != 'A': continue
        tl = data[i-1][j-1]
        tr = data[i-1][j+1]
        bl = data[i+1][j-1]
        br = data[i+1][j+1]
        count += ((tl == 'S' and br == 'M') or (tl == 'M' and br == 'S')) and ((tr == 'S' and bl == 'M') or (tr == 'M' and bl == 'S'))
        # tl_br = data[i-1][j-1] + data[i][j] + data[i+1][j+1]
        # tr_bl = data[i-1][j+1] + data[i][j] + data[i+1][j-1]
        # print((i, j), tl_br, tr_bl)
        # count += (tl_br == 'MAS' or tl_br == 'SAM') and (tr_bl == 'MAS' or tl_br == 'SAM')
print(count)
