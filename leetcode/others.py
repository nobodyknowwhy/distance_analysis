import pandas as pd

df = pd.read_csv(r"a.csv")

df = df.fillna(100)

columns = ['1604“妮妲”', '1522“彩红”', '1415“海鸥”', '1409“威马逊”', '1311“尤特”',
       '1213“启德”', '1208“韦森特”', '0907“天鹅”', '0915“巨爵”', '1822“山竹”', '1713“天鸽”',
       '1832“百里嘉”']


# 统计所有数值中大于 0.15 的数量
count_greater_than_0_15 = (df[columns] < 0.5).sum().sum()  # 对所有列进行统计
print("大于 0.15 的数值数量：", count_greater_than_0_15)

# 统计所有非零数值的数量
count_non_zero = (df[columns] != 100).sum().sum()  # 对所有列进行统计
print("非零数值的数量：", count_non_zero)

# 计算比例
proportion = count_greater_than_0_15 / count_non_zero
print("大于 0.15 的数值占所有非零数值的比例：", proportion)

