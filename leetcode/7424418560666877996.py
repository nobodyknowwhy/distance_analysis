def solution(n: int, H: int, A: int, h: list, a: list) -> int:
    # PLEASE DO NOT MODIFY THE FUNCTION SIGNATURE
    # write code here

    monsters = []
    for i in range(n):
        if h[i] < H and a[i] < A:
            monsters.append((h[i], a[i]))

    if not monsters:
        return 0
    else:
        max_len = 1
        dp = [1] * len(monsters)
        for i in range(len(monsters)):
            for j in range(i):
                if monsters[j][0] < monsters[i][0] and monsters[j][1] < monsters[i][1]:
                    if dp[j] + 1 > dp[i]:
                        dp[i] = dp[j] + 1
            if dp[i] > max_len:
                max_len = dp[i]

        return max_len

if __name__ == '__main__':
    print(solution(3, 4, 5, [1, 2, 3], [3, 2, 1]) == 1)
    print(solution(5, 10, 10, [6, 9, 12, 4, 7], [8, 9, 10, 2, 5]) == 2)
    print(solution(4, 20, 25, [10, 15, 18, 22], [12, 18, 20, 26]) == 3)
    print(solution(13, 8, 7, [8,4,1,5,11,8,8,8,3,2,13,1,16], [16,7,6,7,8,1,9,14,14,3,12,14,11]) == 1)
    print(solution(17, 17, 14, [7,9,4,13,5,17,11,8,8,8,16,15,14,1,3,5,9], [4,16,12,16,14,7,2,8,13,14,9,6,10,8,15,12,6]) == 3)
    print(solution(13, 17, 14, [2,3,12,13,7,8,5,15,1,12,17,14,4], [13,13,8,15,2,5,7,8,13,7,6,8,1]) == 4)
