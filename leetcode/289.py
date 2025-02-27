board = [[0,1,0],[0,0,1],[1,1,1],[0,0,0]]

import copy
board_re = copy.deepcopy(board)

num_row = len(board_re)

num_col = len(board_re[0])

for x in board_re:
    x.insert(0, 0)
    x.append(0)

board_re.insert(0, [0 for _ in range(num_col + 2)])
board_re.append([0 for _ in range(num_col + 2)])

for x in range(1, len(board_re) - 1):
    for y in range(1, len(board_re[0]) - 1):
        count_1 = 0
        if board_re[x - 1][y] == 1:
            count_1 += 1
        if board_re[x][y - 1] == 1:
            count_1 += 1
        if board_re[x - 1][y - 1] == 1:
            count_1 += 1
        if board_re[x - 1][y + 1] == 1:
            count_1 += 1
        if board_re[x + 1][y - 1] == 1:
            count_1 += 1
        if board_re[x + 1][y + 1] == 1:
            count_1 += 1
        if board_re[x + 1][y] == 1:
            count_1 += 1
        if board_re[x][y + 1] == 1:
            count_1 += 1

        if count_1 < 2:
            board[x - 1][y - 1] = 0
        if count_1 == 2:
            board[x - 1][y - 1] = board_re[x][y]
        if count_1 == 3:
            board[x - 1][y - 1] = 1
        if count_1  > 3:
            board[x - 1][y - 1] = 0

print(board)




