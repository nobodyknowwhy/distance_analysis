def built_pmt(pattern):
    pmt = [0 for _ in pattern]
    y = 0
    for x in range(1, len(pattern)):

        while y > 0 and pattern[x] != pattern[y]:
            y = pmt[y - 1]

        if pattern[x] == pattern[y]:
            y += 1
            pmt[x] = y
        else:
            pmt[x] = 0

    return pmt


def kmp_alg(text, pattern):
    m = len(pattern)
    pmt = built_pmt(pattern)

    j = 0
    count = 0
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = pmt[j - 1]

        if text[i] == pattern[j]:
            j += 1
        if j == m:
            count += 1
            #
            j = pmt[j - 1]

    return count


print(kmp_alg("alalakdhiugfkallalgalagkdbkjgfhkuahduhwduihgfkalhalkfhafuuw", "ala"))
