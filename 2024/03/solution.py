import re
from pathlib import Path

folder = Path(__file__).parent

with open(folder / 'input.txt') as handle:
    data = handle.read()

matcher = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')
print(sum(int(m[1]) * int(m[2]) for m in matcher.finditer(data)))

matcher2 = re.compile(r"(mul)\((\d{1,3}),(\d{1,3})\)|(do)\(\)|(don't)\(\)")
on = True
total = 0
for m in matcher2.finditer(data):
    if m[1] == 'mul' and on:
        total += int(m[2]) * int(m[3])
    elif m[4] == 'do':
        on = True
    elif m[5] == "don't":
        on = False

print(total)
