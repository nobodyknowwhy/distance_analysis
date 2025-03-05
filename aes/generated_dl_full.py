import pandas as pd
import pandasql as psql


df = pd.read_csv(r"D:\gs\distance_analysis\aes\dataset\ELLIPSE-Corpus\ELLIPSE_Final_github_train.csv")

query = """select full_text, Overall from df where prompt='Distance learning'"""

res = psql.sqldf(query, env=locals())

res.to_csv(r"D:\gs\distance_analysis\aes\dataset\ELLIPSE-Corpus\dl_full.csv", index=False)