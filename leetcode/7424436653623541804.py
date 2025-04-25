def solution(n: int, u: list) -> int:

    min_num = min(u)

    return len([x for x in u if x != min_num])

if __name__ == '__main__':
    print(solution(n = 5, u = [1, 2, 3, 1, 2]) == 3)
    print(solution(n = 4, u = [100000, 100000, 100000, 100000]) == 0)
    print(solution(n = 6, u = [1, 1, 1, 2, 2, 2]) == 3)