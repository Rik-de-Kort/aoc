with open('input') as handle:
    coords, folding = handle.read().split('\n\n')
    coords = [line.strip().split(',') for line in coords.split('\n')]
    paper = {(int(x), int(y)) for x, y in coords}
    instructions = [line.strip('fold along ').split('=') for line in folding.split('\n') if line]
    instructions = [(direction, int(value)) for direction, value in instructions]

def fold_x(x_fold, paper):
    new_paper = set()
    for x, y in paper:
        if x < x_fold: new_paper.add((x,y))
        elif x > x_fold: new_paper.add((x_fold-(x-x_fold), y)) 
        else: print(f'uh-oh, {x, y} on folding line')
    return new_paper

def fold_y(y_fold, paper):
    new_paper = set()
    for x, y in paper:
        if y < y_fold: new_paper.add((x, y))
        elif y > y_fold: new_paper.add((x, y_fold-(y-y_fold)))
        else: print(f'uh-oh, {x, y} on folding line')
    return new_paper

def print_paper(paper):
    max_x = max(x for x, y in paper) + 1
    max_y = max(y for x, y in paper) + 1
    result = []
    for y in range(max_y):
        result.append(''.join('#' if (x, y) in paper else '.' for x in range(max_x)))
    print('\n'.join(result))

for direction, place in instructions:
    if direction == 'x':
        paper = fold_x(place, paper)
    else:
        paper = fold_y(place, paper)

print_paper(paper)
