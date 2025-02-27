from collections import Counter

s = "paper"
t = "title"

a_list = []
b_list = []

for key, value in Counter(s).items():
    a_list.append(value)

for key, value in Counter(t).items():
    b_list.append(value)

print(a_list == b_list)