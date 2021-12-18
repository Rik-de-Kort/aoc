with open('input') as handle:
    data = [int(line.strip()) for line in handle.readlines() if line.strip()]


# data = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
windows = [sum(data[i:i+3]) for i in range(len(data)-2)]
print(len(data))
print(len(windows))
# print(windows)

print(sum(first < second for first, second in zip(windows[:-1], windows[1:])))
