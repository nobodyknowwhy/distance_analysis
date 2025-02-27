matrix = [[1,2,3],[4,5,6],[7,8,9]]

import numpy as np

matrix = list(np.array(matrix).T)

for i, x in enumerate(matrix):
    x = list(x)
    matrix[i] = x[::-1]

print(matrix)