import pandas as pd
from pandasql import sqldf

df = pd.read_csv(r"D:\gs\distance_analysis\aes\out\first_clean\test\aes_lw_dl_with_vocab_1c.csv")


print(df['text'][0])