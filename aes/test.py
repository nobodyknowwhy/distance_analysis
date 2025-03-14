import pandas as pd
from pandasql import sqldf

df = pd.read_csv(r"D:\gs\distance_analysis\aes\out\test\aes_g_c_v_1clean_c_with_vocab.csv")


query = """select * from df where abs(score-Vocabulary) < 2"""

res = sqldf(query, locals())

res.to_csv(r"D:\gs\distance_analysis\aes\out\test\aes_g_c_v_1clean_cv.csv", index=False)

print(res)
