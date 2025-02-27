def solution(S: str, T: str) -> int:
    # PLEASE DO NOT MODIFY THE FUNCTION SIGNATURE
    # write code here
    delete_num = len(S) - len(T) if len(S) > len(T) else 0
    change_num = 0
    for x in range(min(len(S), len(T))):
        if S[x] != T[x]:
            change_num += 1

    return change_num + delete_num

if __name__ == '__main__':
    print(solution("aba", "abb") == 1)
    print(solution("abcd", "efg") == 4)
    print(solution("xyz", "xy") == 1)
    print(solution("hello", "helloworld") == 0)
    print(solution("same", "same") == 0)