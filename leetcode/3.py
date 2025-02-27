s = 'askhhhdaskjwhh'
now_list = []
len_now = 0
len_max = 0
left_point, right_point = 0, 0
for x in range(0, len(s)):
    if s[x] not in now_list:
        now_list.append(s[x])
        len_now += 1
        right_point += 1
        len_max = max(len_now, len_max)
    else:
        mark = s[x]
        for y in range(left_point, right_point + 1):
            if mark in now_list:
                now_list.pop(0)
                len_now -= 1
                left_point += 1

        now_list.append(mark)
        len_now += 1
        right_point += 1

print(len_max)