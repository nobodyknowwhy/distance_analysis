import re
a = '选择："我会指挥他们的行动。;我会确保战术的执行。(分支：1;2)"'

b = '选择："他们很可能会利用萨卡兹对于源石的古老研究。;时间不多，我们需要快速确认行军路线。(分支：1;2)"'

c = '选择："直面战场是我们唯一的选择。(分支：1)"'

list_tmp = []
list_tmp.append(a)
list_tmp.append(b)
list_tmp.append(c)

for line in list_tmp:
    if line.startswith('选择'):
        npc_name = '博士'

        npc_line = re.sub('[：，。！\.——？]*?', r'', line)

        print(npc_line)
