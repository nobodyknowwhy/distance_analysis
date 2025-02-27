matrix = [[1,2,3,4],[5,0,7,8],[0,10,11,12],[13,14,15,0]]

mark_heng = {}

mark_lie = {}

for x in range(0, len(matrix)):
    for y in range(len(matrix[0])):
        if matrix[x][y] == 0:
            mark_heng[x] = ''
            mark_lie[y] = ''

for x in range(0, len(matrix)):
    for y in range(len(matrix[0])):
        if x in mark_heng or y in mark_lie:
            matrix[x][y] = 0

print(matrix)