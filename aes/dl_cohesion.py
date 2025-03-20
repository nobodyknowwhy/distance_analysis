import re

import numpy as np
from matplotlib import pyplot as plt
from nltk.tokenize import sent_tokenize, word_tokenize
from scipy.optimize import curve_fit
from sympy import floor

# 定义参考词和过渡词列表
REFERENCE_WORDS = ["else", "but", "also", "then", "although", "thus", "therefore", "therefore", "however", "furthermore", "moreover", "additionally",
    "consequently", "similarly", "meanwhile", "on the other hand", "in contrast", "not only", "in addition", "for instance", "while", "since", "unless", "in my opinion", "for example", "but also"]
TRANSITIONAL_WORDS = [
   "who", "whom", "whose","which", "when", "whether", "what", "where", "how", "why", "that"
]


def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def preprocess_text(text):
    paragraphs = text.split("\n")
    sentences = [sentence.strip() for paragraph in paragraphs for sentence in sent_tokenize(paragraph)]
    return paragraphs, sentences


def analyze_connectors(text):
    words = [word.lower() for word in word_tokenize(text)]

    reference_count = sum(1 for word in words if word in REFERENCE_WORDS)

    total_words = len(words)

    return reference_count, total_words


def analyze_connectors_sent(text):
    sentences = [sent.lower() for sent in sent_tokenize(text)]

    advance_connection = 0
    for sent in sentences:
        pattern = r'(,\s[a-zA-Z]+ing)|(^[a-zA-Z]+ing)'

        matches = re.findall(pattern, sent)

        if matches:
            advance_connection += 1

        else:
            for word in TRANSITIONAL_WORDS:
                if word in sent:
                    advance_connection += 1
                    break


    return advance_connection, len(sentences)


def evaluate_text_organization(text):
    reference_count, total_words = analyze_connectors(text)

    connector_ratio = (reference_count) / total_words

    score = connector_ratio

    return score


def evaluate_text_organization_by_sent(text):
    advance_connection, total_sentence = analyze_connectors_sent(text)
    connector_sent_ratio = advance_connection / total_sentence
    score = connector_sent_ratio

    return score


import pandas as pd
from pandasql import sqldf

df = pd.read_csv(r"D:\gs\distance_analysis\aes\dataset\ELLIPSE-Corpus\dl_sample.csv")
df['new_coh'] = df['full_text'].apply(lambda text: evaluate_text_organization(text))
df['new_coh2'] = df['full_text'].apply(lambda text: evaluate_text_organization_by_sent(text))

query = """select Cohesion, new_coh, new_coh2 from df"""

res = sqldf(query, env=locals())

# res = res.drop([3, 8])

res['Cohesion'] = res['Cohesion'].apply(lambda x: int(floor(x)))

print(res)


def func_3wei(xy, a, b, c):
    x, y = xy
    return a * x + b * y + c


popt, pcov = curve_fit(func_3wei, (res['new_coh'].values, res['new_coh2'].values), res['Cohesion'].values)

a, b, c = popt

print(a, b, c)

test_list = [(0.01 * x, (0.1 + 0.1 * x)) for x in range(8)]

print(f"{a}, {b}, {c}")

for x in test_list:
    print(func_3wei(x, a, b, c))

print("***********************")
print(func_3wei((0.02, 0.3), a, b, c))
print(func_3wei((0.07, 0.02), a, b, c))

df_tar = pd.read_csv(r"D:\gs\distance_analysis\aes\out\second_clean\test\aes_g_c_v_2clean_full_vg.csv")


def add_coh(text: str, a, b, c, model_fun) -> int:
    div1 = evaluate_text_organization(text)

    div2 = evaluate_text_organization_by_sent(text)

    value = model_fun((div1, div2), a, b, c)

    if value < 1:
        value = 1
    if value > 5:
        value = 5

    return int(round(value))


df_tar = df_tar.dropna(ignore_index=True)
from tqdm import tqdm

tqdm.pandas(desc="进度")
df_tar['Cohesion'] = df_tar['text'].progress_apply(lambda x: add_coh(x, a, b, c, func_3wei))

print(df_tar)

# df_tar.to_csv(r"D:\gs\distance_analysis\aes\out\second_clean\test\aes_g_c_v_2clean_full_vgc.csv", index=False)

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

x = np.linspace(res['new_coh'].min(), res['new_coh'].max(), 100)
y = np.linspace(res['new_coh2'].min(), res['new_coh2'].max(), 100)
X, Y = np.meshgrid(x, y)

# 绘制图形
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# 绘制原始数据点
ax.scatter(res['new_coh'], res['new_coh2'], res['Cohesion'], c='b', marker='o', label='源数据')

# 绘制拟合曲面
ax.plot_surface(X, Y, func_3wei((X,Y),a, b, c)
                , cmap='viridis', alpha=0.5, label='拟合平面')

# 添加标签和标题
ax.set_xlabel('连贯词，短语使用频率')
ax.set_ylabel('连贯句使用频率')
ax.set_zlabel('文章句法使用，连贯度得分')
ax.set_title('3D拟合平面')

ax.legend()

plt.show()