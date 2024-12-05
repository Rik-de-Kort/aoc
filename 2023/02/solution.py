with open('input') as handle:
    data = [line.strip().split() for line in handle.readlines()]

print(data[:10])
print(set(c for c, _ in data))

x, y, aim = 0, 0, 0

for command, amount in data:
    if command == 'forward':
        x += int(amount)
        y += int(amount) * aim
    elif command == 'down':
        aim += int(amount)
    elif command == 'up': 
        aim -= int(amount)

print(x * y)
