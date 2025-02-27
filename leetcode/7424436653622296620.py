def solution(n: int, k: int) -> int:
    # PLEASE DO NOT MODIFY THE FUNCTION SIGNATURE
    # write code here


    return sum([k * (x + 1) for x in range(n)])

if __name__ == '__main__':
    print(solution(n = 3, k = 1) == 6)
    print(solution(n = 2, k = 2) == 6)
    print(solution(n = 4, k = 3) == 30)