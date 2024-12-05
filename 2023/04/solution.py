with open('input') as handle:
    numbers, *boards = handle.read().split('\n\n')


numbers = [int(x) for x in numbers.split(',')]
boards = [[[int(x) for x in row.split()] for row in board.split('\n') if row] for board in boards]

for board in boards:
    if set(len(row) for row in board) != {5}:
        print(board)

assert all(set(len(row) for row in board) == {5} for board in boards) and all(len(board) == 5 for board in boards)

def bingo(board, prefix):
    return (any(all(x in prefix for x in row) for row in board) 
            or any(all(x in prefix for x in column) for column in zip(*board)))


boards = dict(enumerate(boards))
for i in range(5, len(numbers)):
    prefix = numbers[:i]
    to_delete = []
    for i, board in boards.items():
        if bingo(board, prefix):
            to_delete.append(i)
            if len(boards) == len(to_delete):
                print(sum(x for row in board for x in row if x not in prefix) * prefix[-1])
    for i in to_delete: del boards[i]

