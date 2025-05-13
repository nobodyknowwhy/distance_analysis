import os

file_path = r'D:\工作交接材料汇总\WSXS2024038海南'


count_p = 0
for a,b,c in os.walk(file_path):

    count_p += len(c)


print(count_p)
