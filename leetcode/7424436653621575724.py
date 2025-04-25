def solution(n: int, a: list) -> list:
    out_list = []
    while True:
        out_list.append(a.pop(0))
        if not a:
            break
        a.append(a.pop(0))

    return out_list

if __name__ == '__main__':
    print(solution(n = 5, a = [5, 3, 2, 1, 4]) == [5, 2, 4, 1, 3])
    print(solution(n = 4, a = [4, 1, 3, 2]) == [4, 3, 1, 2])
    print(solution(n = 6, a = [1, 2, 3, 4, 5, 6]) == [1, 3, 5, 2, 6, 4])