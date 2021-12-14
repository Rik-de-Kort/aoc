with open('input') as handle:
    data = [int(s) for s in handle.read().strip().split(',')]

lfs = [sum(lf ==i for lf in data) for i in range(0, 9)]
print(lfs)
for day in range(256+1):
    spawned = lfs[0]
    for i in range(0, 8): lfs[i] = lfs[i+1]
    lfs[8] = spawned
    lfs[6] += spawned

print(sum(lfs[:8]))
