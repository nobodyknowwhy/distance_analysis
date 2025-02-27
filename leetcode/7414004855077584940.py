def solution(n, max, array):
    # Edit your code here
    from collections import Counter
    counter_result = Counter(array)

    tuple_all_b = sorted([key for key, value in counter_result.items() if value >= 2 and 2 * key < max], reverse=True)

    tuple_all_a = sorted([key for key, value in counter_result.items() if value >= 3 and 3 * key < max], reverse=True)

    if 1 in tuple_all_a:
        tuple_all_a.pop(-1)
        tuple_all_a.insert(0, 1)

    if 1 in tuple_all_b:
        tuple_all_b.pop(-1)
        tuple_all_b.insert(0, 1)

    for x in tuple_all_a:
        for y in tuple_all_b:
            if 3 * x + 2 * y <= max and x != y:
                return [x, y]

    return [0, 0]


if __name__ == "__main__":
    # Add your test cases here

    print(solution(9, 34, [6, 6, 6, 8, 8, 8, 5, 5, 1]) == [8, 5])
    print(solution(9, 37, [9, 9, 9, 9, 6, 6, 6, 6, 13]) == [6, 9])
    print(solution(9, 40, [1, 11, 13, 12, 7, 8, 11, 5, 6]) == [0, 0])
