s = "a"
t = "a"


def solution(s: str, t: str) -> str:
    from collections import Counter

    s_counter = Counter(s)

    t_counter = Counter(t)

    for key, value in t_counter.items():
        if key in s_counter:
            if s_counter[key] - t_counter[key] < 0:
                return ''
        else:
            return ''

    min_len = 100
    min_str = ''
    for x in range(0, len(s)):
        if s[x] in t:
            for end_index in range(x, len(s)):
                tmp_t_counter = t_counter
                a = tmp_t_counter - Counter(s[x:end_index + 1])
                if len(a) == 0:
                    if end_index - x < min_len:
                        min_str = s[x:end_index + 1]
                        min_len = len(min_str)
                    break

    return min_str


if __name__ == '__main__':
    print(solution(s, t))
