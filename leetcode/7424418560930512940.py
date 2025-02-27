def get_qian_by_num(s:str):
    try:
        s = str(eval(s))
    except Exception as e:
        s = str(int(eval(s + '.0')))

    num_list = s.split('.')

    if len(num_list) == 2:

        target_s = '.' + num_list[1]
        count_3 = 0
        for x in num_list[0][::-1]:
            count_3 += 1
            target_s = x + target_s
            if count_3 == 3:
                target_s = ',' + target_s
                count_3 = 0
    else:
        target_s = ''
        count_3 = 0
        for x in num_list[0][::-1]:
            count_3 += 1
            target_s = x + target_s
            if count_3 == 3:
                target_s = ',' + target_s
                count_3 = 0

    return target_s[1:] if target_s.startswith(',') else target_s


if __name__ == '__main__':
    a = get_qian_by_num('02300545202')

    print(a)