matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]

num_rows = len(matrix)
num_cols = len(matrix[0])

matrix_mark = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

out_list = []
out_len = 0
x = 0
y = 0
out_list.append(matrix[x][y])
matrix_mark[x][y] = 1
while True:
    for y in range(y + 1, num_cols):
        if not matrix_mark[x][y]:
            out_list.append(matrix[x][y])
            matrix_mark[x][y] = 1
        else:
            y -= 1
            break

    for x in range(x + 1, num_rows):
        if not matrix_mark[x][y]:
            out_list.append(matrix[x][y])
            matrix_mark[x][y] = 1
        else:
            x -= 1
            break

    for y in range(y - 1, -1, -1):
        if not matrix_mark[x][y]:
            out_list.append(matrix[x][y])
            matrix_mark[x][y] = 1
        else:
            y += 1
            break

    for x in range(x - 1, -1, -1):
        if not matrix_mark[x][y]:
            out_list.append(matrix[x][y])
            matrix_mark[x][y] = 1
        else:
            x += 1
            break

    if out_len != len(out_list):
        out_len = len(out_list)
    else:
        break

print(out_list)