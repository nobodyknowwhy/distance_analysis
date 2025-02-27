intervals = [[1,3],[2,6],[8,10],[15,18]]

numbers = [num for sublist in intervals for num in sublist]

print(numbers)