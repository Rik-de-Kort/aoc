from pathlib import Path
import re

folder = Path(__file__).parent

with open(folder / 'input.txt') as handle:
    data = [line.strip() for line in handle.readlines()]

i_max = len(data)
j_max = len(data[0])

matcher = re.compile('XMAS')

def find_matches(data):
    return sum(len(matcher.findall(line)) for line in data)


print('\n'.join(data))
print(find_matches(data))
print('-'*15)

reversed =[ ''.join(reversed(line)) for line in data]
print('\n'.join(reversed))
print(find_matches(reversed))

transposed = [''.join(line) for line in zip(*data)]
print('\n'.join(transposed))
print(find_matches(transposed))

# # print(sum(len(matcher.findall(line)) for line in data))
# # print(sum(len(matcher.findall(''.join(reversed(line)))) for line in data))
# # diagonals = [''.join(data[i+k][j+k] for k in range(min(i_max-i-1, j_max-j-1))) for i in range(0, i_max) for j in range(0, j_max)]
# # print(sum(len(matcher.findall(line)) for line in diagonals))
# # print(sum(len(matcher.findall(''.join(reversed(line)))) for line in diagonals))
# #
#
# transposed = [''.join(line) for line in zip(*data)]
#
