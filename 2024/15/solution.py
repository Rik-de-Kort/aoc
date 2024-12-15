from copy import deepcopy
from pathlib import Path

folder = Path(__file__).parent

with open(folder / 'input.txt') as handle:
    raw_warehouse, moves = handle.read().split('\n\n')
    warehouse = {}
    robot = 0
    for i, line in enumerate(raw_warehouse.split('\n')):
        for j, c in enumerate(line):
            if c == '@':
                robot = i + j * 1j
                warehouse[i + j * 1j] = '.'
            elif c in ('#', 'O'):
                warehouse[i + j * 1j] = c
    moves = [move for move in moves if move in ('v', '<', '>', '^')]


def display(warehouse, robot):
    i_max = max(int(z.real) + 1 for z in warehouse.keys())
    j_max = max(int(z.imag) + 1 for z in warehouse.keys())
    lines = [' ' + ''.join(str(j % 10) for j in range(j_max))]
    for i in range(i_max):
        line = [str(i)]
        for j in range(j_max):
            if robot == i + j * 1j:
                line.append('@')
            else:
                line.append(warehouse.get(i + j * 1j, '.'))
        lines.append(line)
    print('\n'.join(''.join(line) for i, line in enumerate(lines)))


def step(warehouse, robot, move):
    direction = -1j if move == '<' else 1j if move == '>' else -1 if move == '^' else 1 if move == 'v' else 1000
    if direction == 1000:
        raise ValueError((move, int(move)))
    if warehouse.get(robot + direction, '.') == '.':
        robot += direction
        return warehouse, robot

    n_boxes = 0
    while warehouse.get(robot + (n_boxes + 1) * direction) == 'O':
        n_boxes += 1

    if warehouse.get(robot + (n_boxes + 1) * direction, '.') == '.':
        # Remove box right in front
        del warehouse[robot + direction]
        # Boxes all shift by one:
        # robot + 1*direction -> robot + 2*direction
        # robot + 2*direction -> robot + 3*direction
        # ...
        for i in range(n_boxes):
            warehouse[robot + (i + 2) * direction] = 'O'

        robot += direction
        return warehouse, robot
    elif warehouse.get(robot + (n_boxes + 1) * direction, '.') == '#':
        # no move
        return warehouse, robot
    else:
        print("=" * 100)
        print(f'Error with {robot=}, trying to move {move=} ({direction=}')
        display(warehouse, robot)
        print(f'Easier debug:\n{(robot, warehouse, direction)=}')
        print('=' * 100)
        raise ValueError(warehouse, robot, move)


# display(warehouse, robot)
for move in moves:
    warehouse, robot = step(warehouse, robot, move)
    # print(f'Move {move}:')
    # display(warehouse, robot)
    # print('')

display(warehouse, robot)
print(sum(int(z.real) * 100 + int(z.imag) for z, c in warehouse.items() if c == 'O'))

with open(folder / 'input.txt') as handle:
    raw_warehouse, _ = handle.read().split('\n\n')
    warehouse = {}
    robot = 0
    for i, line in enumerate(raw_warehouse.split('\n')):
        for j, c in enumerate(line):
            if c == '@':
                robot = i + j * 2j
            if c in ('@', '.'):
                warehouse[i + j * 2j + 0j] = '.'
                warehouse[i + j * 2j + 1j] = '.'
            elif c == '#':
                warehouse[i + j * 2j + 0j] = '#'
                warehouse[i + j * 2j + 1j] = '#'
            elif c == 'O':
                warehouse[i + j * 2j + 0j] = '['
                warehouse[i + j * 2j + 1j] = ']'


def step2(warehouse, robot, move):
    if move == '<':
        direction = -1j

        n_boxes = 0
        while warehouse.get(robot + (2 * n_boxes + 1) * direction) == ']':
            n_boxes += 1

        if warehouse.get(robot + (2 * n_boxes + 1) * direction) == '#':
            return warehouse, robot

        if robot + direction in warehouse:
            del warehouse[robot + direction]
        # First box at robot + 1 * direction -> robot + 2 * direction
        # Second box at robot + 3 * direction -> robot + 4 * direction
        # Third box at robot + 5 direction -> robot + 6 * direction
        for i in range(n_boxes):
            warehouse[robot + ((i + 1) * 2 + 0) * direction] = ']'
            warehouse[robot + ((i + 1) * 2 + 1) * direction] = '['

        robot += direction
        return warehouse, robot
    elif move == '>':
        direction = 1j

        n_boxes = 0
        while warehouse.get(robot + (2 * n_boxes + 1) * direction) == '[':
            n_boxes += 1

        if warehouse.get(robot + (2 * n_boxes + 1) * direction) == '#':
            return warehouse, robot

        if robot + direction in warehouse:
            del warehouse[robot + direction]
        # First box at robot + 1 * direction -> robot + 2 * direction
        # Second box at robot + 3 * direction -> robot + 4 * direction
        # Third box at robot + 5 direction -> robot + 6 * direction
        for i in range(n_boxes):
            warehouse[robot + ((i + 1) * 2 + 0) * direction] = '['
            warehouse[robot + ((i + 1) * 2 + 1) * direction] = ']'

        robot += direction
        return warehouse, robot
    elif move == 'v' or move == '^':
        direction = 1 if move == 'v' else -1

        boxes = set()
        frontier = [robot + direction]
        while any(warehouse.get(point, '.') in '[]' for point in frontier):
            new_frontier = []
            for point in frontier:
                if warehouse.get(point) == '[':
                    boxes.add((point + 0j, point + 1j))
                    new_frontier.extend([point + 0j + direction, point + 1j + direction])
                elif warehouse.get(point) == ']':
                    boxes.add((point - 1j, point + 0j))
                    new_frontier.extend([point - 1j + direction, point + 0j + direction])
                else:
                    new_frontier.append(point)
            frontier = new_frontier

        if any(warehouse.get(point) == '#' for point in frontier):
            # no move
            return warehouse, robot

        robot += direction
        assert all(left in warehouse and right in warehouse for left, right in boxes)
        assert all(left != right for left, _ in boxes for __, right in boxes)
        for left, right in boxes:
            if left not in warehouse:
                print('wut')
            del warehouse[left]
            del warehouse[right]
        for left, right in boxes:
            warehouse[left + direction] = '['
            warehouse[right + direction] = ']'

        return warehouse, robot
    else:
        raise ValueError(f'Unknown {move=}')


display(warehouse, robot)
for i, move in enumerate(moves):
    warehouse, robot = step2(warehouse, robot, move)
    # print(f'Move {move}:')
    # display(warehouse, robot)
    # print('')

print(sum(int(100 * z.real + z.imag) for z, c in warehouse.items() if c == '['))
