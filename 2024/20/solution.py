from pathlib import Path

from tqdm import tqdm

folder = Path(__file__).parent

with open(folder / 'input.txt') as handle:
    track = {i + j * 1j: c for i, line in enumerate(handle.readlines()) for j, c in enumerate(line.strip()) if
             line.strip()}

start = [k for k, v in track.items() if v == 'S'][0]
end = [k for k, v in track.items() if v == 'E'][0]

i_min, i_max = 0, int(max(z.real for z in track.keys())) + 1
j_min, j_max = 0, int(max(z.imag for z in track.keys())) + 1


def display(track, route):
    print('\n'.join(
        ''.join('O' if i + j * 1j in route else track[i + j * 1j] for j in range(j_min, j_max))
        for i in range(i_min, i_max)
    ))


def in_bounds(z):
    return i_min <= z.real < i_max and j_min <= z.real < j_max


route = [start]
while route[-1] != end:
    z_next = route[-1] + 1
    for z_next in [route[-1] + 1, route[-1] - 1, route[-1] + 1j, route[-1] - 1j]:
        if z_next not in route and in_bounds(z_next) and track[z_next] != '#':
            route.append(z_next)
            continue

route_index = {z: i for i, z in enumerate(route)}
cheat_start = 1 + 7j
i = route_index[cheat_start]
cheat_moves = [(x, y) for x in [1, -1, 1j, -1j] for y in [1, -1, 1j, -1j] if x + y != 0]
cheats = []
for i, cheat_start in enumerate(route):
    for step1, step2 in cheat_moves:
        gain = route_index.get(cheat_start + step1 + step2, 0) - i - 2
        if gain > 0:
            cheats.append(((cheat_start, cheat_start + step1 + step2), gain))

# display(track, [1+7j])
print(sum(gain >= 100 for _, gain in cheats))


def d(z, w):
    return abs(z.real - w.real) + abs(z.imag - w.imag)


alt_cheats = [(start, end, d(end, start)) for i, start in tqdm(enumerate(route)) for j, end in enumerate(route) if
              j - i - d(end, start) >= 100 and d(end, start) <= 20]
print(len(alt_cheats))
