def solution(word: str) -> int:
    import re

    return len(set([int(x) for x in re.sub('[a-zA-Z]', ' ', word).strip().split()]))

if __name__ == '__main__':
    print(solution("a123bc34d8ef34") == 3)
    print(solution("t1234c23456") == 2)
    print(solution("a1b01c001d4") == 2)