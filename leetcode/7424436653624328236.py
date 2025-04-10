def solution(values: list) -> int:

    len_val = len(values)

    max_val = -1

    for i in range(0, len_val):
        for j in range(i, len_val):
            if i == j:
                tmp_val = values[i]
            else:
                tmp_val = values[i] + values[j] + i - j

            max_val = max(max_val, tmp_val)

    return max_val

if __name__ == '__main__':
    print(solution(values=[8, 3, 5, 5, 6]) == 11)
    print(solution(values=[10, 4, 8, 7]) == 16)
    print(solution(values=[1, 2, 3, 4, 5]) == 8)