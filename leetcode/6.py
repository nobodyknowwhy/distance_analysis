s = "AB"
numRows = 2

start_index = 0

mark_index = []

mark_inverse = False

mark_loop = 0

out_string = ''

if numRows==1:
    print(s)
    exit(0)

for x in range(0, len(s)):
    if not mark_inverse:
        mark_loop += 1
        if mark_loop == numRows:
            mark_inverse = True
        mark_index.append(mark_loop)
    else:
        mark_loop -= 1
        if mark_loop == 1:
            mark_inverse = False
        mark_index.append(mark_loop)

for x in range(1, numRows + 1):
    for y in range(len(mark_index)):
        if mark_index[y] == x:
            out_string += s[y]

print(out_string)