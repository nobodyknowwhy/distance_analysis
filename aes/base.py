import pandas as pd
from pandasql import sqldf

prompt_list = ['Distance learning']

score_list = [1, 2, 3, 4, 5]

standard_list = [
        """
        VG:Numerous vocabulary and grammatical errors seriously impair comprehension,or a low word count reflects only simple use of words and basic sentence patterns;
        LF:Chaotic expressions with multiple inconsistencies;
        EA:Expression is generally in line with the topic.but it isn't easy to understand in a few places.
        """,
        """
        VG:More vocabulary and grammatical errors, but not so any as to detract from overall comprehension; able to use basic sentence pattern correctly;
        LF:Expressions are less fluent,with several disjointed transitions;
        EA:Generally consistent with the topic.
        """,
        """
        VG:Frequent lexical or grammatical errors in complex expressions or predominant use of basic vocabulary and sentence patterns throughout;
        LF:Expressions are fluent, but structural transitions are stiff:
        EA:Generally consistent with the topic, the reader can understand the content.
        """,
        """
        VG:Few lexical or grammatical errors; able to use a variety of vocabulary and sentence types;
        LF:Fluent expression and well-organized content;
        EA:Fully consistent with the topic and able to convey specific information effectively.
        """,
        """
        VG:No lexical or grammatical errors, extensive use of a wide range of vocabulary, and the ability to flexibly use a variety of sentence patterns;
        LF:Fluent and coherent expression with natura transitions and well-organized content structure;
        EA:Fully consistent with the topic and able to convey rich information effectively.
        """
                 ]

df_dl_s = pd.read_csv(r"D:\gs\distance_analysis\aes\dataset\ELLIPSE-Corpus\dl_sample.csv")
sample_text = []

for score in score_list:
    query = f"select * from df_dl_s where Overall={score}"
    sample_text.append(sqldf(query)['full_text'].values[0])
