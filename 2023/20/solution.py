with open('input') as handle:
    algorithm_data, input_image = handle.read().split('\n\n')
    algorithm_data = [x == '#' for x in algorithm_data.strip()]
    input_image = {(i, j): x == '#' for i, line in enumerate(input_image.strip().split('\n')) for j, x in enumerate(line.strip())}

assert len(algorithm_data) == 512, len(algorithm_data)

def print_image(im):
    x0, y0 = (min(x for (x, y), v in im.items() if v), min(y for (x, y), v in im.items() if v))
    x1, y1 = (max(x for (x, y), v in im.items() if v), max(y for (x, y), v in im.items() if v))
    print('\n'.join(''.join('#' if im.get((x, y), False) else '.' for y in range(y0-2, y1+3)) for x in range(x0-2, x1+3)))
    
def enhance(im, algorithm, default=False):
    x0, y0 = (min(x for (x, y), v in im.items() if v), min(y for (x, y), v in im.items() if v))
    x1, y1 = (max(x for (x, y), v in im.items() if v), max(y for (x, y), v in im.items() if v))
    enhanced = {}
    for x in range(x0-4, x1+4+1):
        for y in range(y0-4, y1+4+1):
            indices = [(x-1, y-1), (x-1, y+0), (x-1, y+1),
                       (x+0, y-1), (x+0, y+0), (x+0, y+1),
                       (x+1, y-1), (x+1, y+0), (x+1, y+1)]
            index = int(''.join('1' if im.get(idx, default) else '0' for idx in indices), base=2)
            enhanced[x, y] = algorithm[index]
    return enhanced, not default if algorithm[0] else default

default = False
enhanced = input_image
for _ in range(2):
    enhanced, default = enhance(enhanced, algorithm_data, default=default)
print(sum(enhanced.values()))
for _ in range(48):
    enhanced, default = enhance(enhanced, algorithm_data, default=default)
print(sum(enhanced.values()))
