from collections import Counter 

with open('input') as handle:
    data = [line.strip() for line in handle.readlines()]

counts = [Counter(bits) for bits in zip(*data)]
gamma = int(''.join('1' if c['1'] > c['0'] else '0' for c in counts), base=2)
epsilon = int(''.join('1' if c['1'] < c['0'] else '0' for c in counts), base=2)
print(gamma * epsilon)

def most_common_bit(bits):
    c = Counter(bits)
    assert set(c.keys()) <= {'0', '1'}, set(c.keys())
    return '0' if c['0'] > c['1'] else '1'

candidates = data
bit_index = 0
for bit_index in range(0, max(len(line) for line in data)):
    c = Counter([line[bit_index] for line in candidates])
    b = max(c.keys(), key=lambda x: c[x])
    candidates = [line for line in candidates if line[bit_index] == b]

print(candidates)

candidates = data
bit_index = 0
for bit_index in range(0, max(len(line) for line in data)):
    c = Counter([line[bit_index] for line in candidates])
    b = '1' if c['1'] >= c['0'] else '0'  # most common, keep 1
    candidates = [line for line in candidates if line[bit_index] == b]

print(candidates)
oxygen = int(candidates[0], base=2)
print(oxygen)

candidates = data
bit_index = 0
for bit_index in range(0, max(len(line) for line in data)):
    c = Counter([line[bit_index] for line in candidates])
    if set(c.keys()) == {'0', '1'}:
        b = '0' if c['0'] <= c['1'] else '1'  # least common, keep 0
    else:
        b = list(c.keys())[0]
    candidates = [line for line in candidates if line[bit_index] == b]

print(candidates)
co2 = int(candidates[0], base=2)
print(co2)

print(oxygen*co2)
