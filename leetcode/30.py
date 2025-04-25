def find_sub_str(s, words):
    from collections import Counter
    for word in words:
        if not word in s:
            return []

    len_windows = len(''.join(words))

    len_word = len(words[0])

    len_words = len(words)

    out_list = []

    if len(s) < len_windows:
        return []

    for i in range(0, len(s) - len_windows + 1):
        dict_tar = {}
        words_windows = [s[i + x * len_word:i + (x + 1) * len_word] for x in range(len_words)]

        for x in words_windows:
            if x in s and x in dict_tar:
                dict_tar[x] += 1
            else:
                dict_tar[x] = 1

        if dict(Counter(words)) == dict_tar:
            out_list.append(i)

    return out_list


print(find_sub_str("barfoothefoobarman", ["foo","bar"]))
