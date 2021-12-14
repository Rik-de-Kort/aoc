with open('input') as handle:
    data = [line.strip() for line in handle.readlines()]

braces = {'(': ')', '{': '}', '[': ']', '<': '>'}
scores = {')': 1, ']': 2, '}': 3, '>': 4}
line_scores = []
for line in data:
    score = 0
    stack = []
    for char in line:
        if char in braces:
            stack.append(braces[char])
            continue
        expected = stack.pop()
        if char != expected: break  # Breaks inner loop
    else:  # Runs if for-loop was not broken out of
        for char in reversed(stack):
            score = score * 5 + scores[char]
        line_scores.append(score)

n = int(len(line_scores) / 2)
print(sorted(line_scores)[n])

