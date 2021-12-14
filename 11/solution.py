with open('input') as handle:
    octopi = {(x, y): int(v) for x, line in enumerate(handle.readlines()) for y, v in enumerate(line.strip())}

def neighbours(x, y):
    xs = [x+1] if x == 0 else [x-1] if x==9 else [x-1, x+1]
    ys = [y+1] if y == 0 else [y-1] if y==9 else [y-1, y+1]
    return [(x, y_) for y_ in ys] + [(x_, y) for x_ in xs] + [(x_, y_) for y_ in ys for x_ in xs]

i = 0
flash_count = 0
flashed = set()
while len(flashed) != len(octopi):
    for p in octopi.keys(): octopi[p] += 1

    flashed = set()
    while (to_flash := {p for p, v in octopi.items() if v > 9 and p not in flashed}):
        p = to_flash.pop()
        for q in neighbours(*p): octopi[q] += 1
        flashed.add(p)
    for p in flashed: octopi[p] = 0

    flash_count += len(flashed)
    i += 1
    if i == 100: print(flash_count)

print(i)
