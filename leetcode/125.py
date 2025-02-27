s = "0P"

s_true = ''.join([x for x in s.lower() if x.isalnum()])

mark_half = int(len(s_true)/2)

if len(s_true) % 2 == 0:
    print(s_true[:mark_half] == s_true[mark_half:][::-1])
else:
    print(s_true[:mark_half] == s_true[mark_half + 1:][::-1])