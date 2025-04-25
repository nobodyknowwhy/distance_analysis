def solution(a: int, b: int) -> int:

    a, b = str(a), str(b)

    p = []

    for x in range(len(a)):
        p.append(int(a[:x] + b + a[x:]))

    p.append(int(a + b))
    return max(p)

if __name__ == '__main__':
    # print(solution(0, 1) == 10)
    print(solution(15, 13) == 1513)
