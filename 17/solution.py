with open('input') as handle:
    data = handle.read().split(':')[1].strip()

# data = 'x=20..30, y=-10..-5'
print(data)
(x_start, x_end), (y_end, y_start) = [tuple(int(x) for x in item.split('=')[1].split('..')) for item in data.split(', ')]

def step(x, y, xv, yv):
    x += xv
    y += yv
    xv = xv - 1 if xv > 0 else xv + 1 if xv < 0 else xv
    yv = yv - 1
    return x, y, xv, yv

def hit(x, y):
    return x_start <= x <= x_end and y_start >= y >= y_end

def simulate(xv, yv):
    x, y = 0, 0
    result = [(x, y)]
    while not hit(x, y) and x <= x_end and y >= y_end:
        x, y, xv, yv = step(x, y, xv, yv)
        result.append((x, y))
    return result, hit(x, y), x > x_end, x <= x_end and y < y_end

hits = []
for attempt in [(x, y) for x in range(-500, 500) for y in range(-500, 500)]:
    result, is_hit, *_ = simulate(*attempt)
    if is_hit: hits.append(attempt)
print(len(hits))
