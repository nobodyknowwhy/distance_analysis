def solution(S: str) -> int:
    # PLEASE DO NOT MODIFY THE FUNCTION SIGNATURE
    # write code here
    from collections import Counter
    counter_num = Counter([x for x in S])
    first_extra = []

    for key, value in counter_num.items():
        first_extra.append(int(value / 2))

        counter_num[key] = int(value / 2) if value % 2 == 0 else int(value / 2) + 1

    now_len = sum([y for x, y in counter_num.items()])
    second_extra = (now_len % 26  + int(now_len / 26)) if now_len > 26 else 0


    print(sum(first_extra) + second_extra)

    return sum(first_extra) + second_extra

if __name__ == '__main__':
    print(solution(S = "abab") == 2)
    print(solution(S = "aaaa") == 2)
    print(solution(S = "abcabc") == 3)
    print(solution(S = "ababasjhclqwihflihalhgklrejglshjfklahuiffgkujgfujlzskjlajljoigheiukwlajlihegkulkahaskjsndllglgkjhkhjhsjghsdjfkbkjgshakjwhuhtzekrohelgohalhfqajfohaoh") == 73)
