from functools import reduce
lst = [2, 3, 4]
result = reduce(lambda x, y: x * y, lst, 1)
print(result)
# 1 * 2 * 3 * 4

