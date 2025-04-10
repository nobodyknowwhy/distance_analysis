def solution(array):

    from collections import Counter

    ar_counter = Counter(array)

    for key, value in ar_counter.items():
        if value > int(len(array) / 2):
            return key

    return 0


if __name__ == "__main__":
    # Add your test cases here

    print(solution([1, 3, 8, 2, 3, 1, 3, 3, 3]) == 3)