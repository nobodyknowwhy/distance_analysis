import pandas as pd

df_g = pd.read_csv(r"D:\gs\distance_analysis\aes\out\test\aes_lw_dl_with_grammar.csv")

df_c = pd.read_csv(r"D:\gs\distance_analysis\aes\out\test\aes_lw_dl_with_coh.csv")

df_i = pd.read_csv(r"D:\gs\distance_analysis\aes\out\test\aes_lw_dl_with_vocab.csv")

df_i['Grammar'] =  df_g['Grammar']
df_i['Cohesion'] = df_c['Cohesion']

print(df_i)
print(df_i.columns)

df_i.to_csv(r"D:\gs\distance_analysis\aes\out\test\aes_lw_dl_with_vcg_2025-3-5.csv")