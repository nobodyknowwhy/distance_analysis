import pandas as pd
from pandasql import sqldf
import datetime

df = pd.read_csv(r'D:\gs\distance_analysis\aes\dataset\ELLIPSE-Corpus\ELLIPSE_Final_github_train.csv')

prompt_list = ['Distance learning', 'Career commitment', 'Success and failure', 'Being busy', 'Positive attitudes']

query = "select * from df where prompt = 'Distance learning'"

print()