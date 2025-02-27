from collections import Counter
ransomNote = "aa"

magazine = "aba"

a = True if not len(Counter(ransomNote) - Counter(magazine)) else False

print(a)