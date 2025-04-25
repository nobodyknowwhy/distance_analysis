def find_sub_str(s, words):
    for word in words:
        if not word in s:
            return []

    len_windows = len(''.join(words))

    len_word = len(words[0])

    len_words = len(words)

    if len(s) < len_windows:
        return []

    for i in range(0, len(s) - len_windows + 1):
        words_windows = [s[i + x * len_word:i + (x + 1) * len_word] for x in range(len_words)]

        print(words_windows)


find_sub_str("barfoothefoobarman", ["foo","bar"])
