import pandas as pd
from pandasql import sqldf

# df = pd.read_csv(r"D:\gs\distance_analysis\aes\out\second_clean\test\aes_g_c_v_2clean_full_vgc.csv")
#
# query = """select * from df where abs(score-Vocabulary) < 2 and abs(score-Grammar) < 2 and abs(score-Cohesion) < 2"""
#
# res = sqldf(query, locals())
#
# res.to_csv(r"D:\gs\distance_analysis\aes\out\second_clean\test\aes_vgc_3clean_full2.csv", index=False)
#
# print(res)
#
# print(res['score'].value_counts())

df = pd.read_csv(r"D:\gs\distance_analysis\aes\dataset\ELLIPSE-Corpus\dl_full.csv")

print(df)
