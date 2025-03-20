import language_tool_python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandasql import sqldf
from scipy.optimize import curve_fit
from tqdm import tqdm

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

tqdm.pandas(desc="进度")
tool = language_tool_python.LanguageTool('en-US')


def model_func_exp(x, a, b, c):
    return a * np.exp(-b * x) + c


def model_func_line(x, k, b):
    return k * x + b


def model_func_2ci(x, a, b, c):
    return a * x * x + b * x + c


def check_grammar_errors(text):
    matches = tool.check(text)
    error_count = len(matches)
    tool.close()  # 关闭工具
    return error_count


def calculate_diversity(text: str) -> float:
    """
    词汇多样性，顾名思义就是文章词汇的多样，返回的是（单词的种类）/（总单词数量），为了防止多样性欺骗，文章应该去除停用词的计量，因为停用词过多文章
    反而会造成无效词汇的冗余，词汇多样性应该要是一个绝对正相关的评分抉择项目，所以应考虑去除停用词。除此之外，还需要融合大小写，Hello和hello应该
    视为同一词，同时不能记录标点或是数字符号

    :param text: 输入文章
    :return: 返回文章的词汇多样性
    """
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords

    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]

    unique_words = sum([1 if len(word) < 8 else 1.5 for word in set(filtered_tokens)])

    lexical_diversity = unique_words / sum([1 if len(word) < 8 else 1.5 for word in set(filtered_tokens)])

    return lexical_diversity


def add_vocab(text: str, a, b, c, model_fun) -> int:
    div = calculate_diversity(text)

    value = model_fun(div, a, b, c)

    if value < 1:
        value = 1
    if value > 5:
        value = 5

    return int(round(value))


def add_grammar(text: str, a, b, c, model_fun) -> int:
    div = check_grammar_errors(text)

    value = model_fun(div, a, b, c)

    if value < 1:
        value = 1
    if value > 5:
        value = 5

    return int(round(value))


def main_run_gram():
    dl_sample = pd.read_csv(r"D:\gs\distance_analysis\aes\dataset\ELLIPSE-Corpus\dl_sample.csv")
    dl_sample['g_error'] = dl_sample['full_text'].progress_apply(lambda x: check_grammar_errors(x))

    query = """select Grammar, g_error from dl_sample"""

    res = sqldf(query=query, env=locals())

    popt, pcov = curve_fit(model_func_exp, res['g_error'].values, res['Grammar'].values)

    a, b, c = popt

    print(popt)

    df_with_vocabulary = pd.read_csv(r"D:\gs\distance_analysis\aes\out\second_clean\test\aes_g_c_v_2clean_full_v.csv")

    df_with_vocabulary = df_with_vocabulary.dropna(ignore_index=True)

    df_with_vocabulary['Grammar'] = df_with_vocabulary['text'].progress_apply(
        lambda x: add_grammar(x, a, b, c, model_func_exp))

    print(df_with_vocabulary)

    df_with_vocabulary.to_csv(r"D:\gs\distance_analysis\aes\out\second_clean\test\aes_g_c_v_2clean_full_vg.csv",
                              index=False)


def main_run_vab():
    dl_sample = pd.read_csv(r"D:\gs\distance_analysis\aes\dataset\ELLIPSE-Corpus\dl_sample.csv")
    dl_sample['vocabulary_p'] = dl_sample['full_text'].progress_apply(lambda x: calculate_diversity(x))

    query = """select Vocabulary, vocabulary_p from dl_sample"""

    res = sqldf(query=query, env=locals())

    popt, pcov = curve_fit(model_func_2ci, res['vocabulary_p'].values, res['Vocabulary'].values)

    a, b, c = popt

    df_with_vocabulary = pd.read_csv(r"D:\gs\distance_analysis\aes\out\second_clean\test\aes_g_c_v_2clean_full.csv")

    df_with_vocabulary = df_with_vocabulary.dropna(ignore_index=True)

    df_with_vocabulary['Vocabulary'] = df_with_vocabulary['text'].progress_apply(
        lambda x: add_vocab(x, a, b, c, model_func_2ci))

    print(df_with_vocabulary)

    df_with_vocabulary.to_csv(r"D:\gs\distance_analysis\aes\out\second_clean\test\aes_g_c_v_2clean_full_v.csv",
                              index=False)


def plot_vab():
    # 读取数据
    dl_sample = pd.read_csv(r"D:\gs\distance_analysis\aes\dataset\ELLIPSE-Corpus\dl_sample.csv")

    # 计算 vocabulary_p
    dl_sample['vocabulary_p'] = dl_sample['full_text'].progress_apply(lambda x: calculate_diversity(x))

    # 准备数据
    X = dl_sample['vocabulary_p'].values
    y = dl_sample['Vocabulary'].values

    # 拟合曲线
    popt, pcov = curve_fit(model_func_2ci, X, y)
    a, b, c = popt

    # 生成拟合曲线的 x 值
    x_fit = np.linspace(min(X), max(X), 100)
    y_fit = model_func_2ci(x_fit, a, b, c)

    # 绘制原始数据点
    plt.scatter(X, y, label='源数据', color='blue', alpha=0.6)

    # 绘制拟合曲线
    plt.plot(x_fit, y_fit, label='拟合曲线', color='red')

    # 标注拟合的点
    for i in range(len(X)):
        plt.text(X[i], y[i], f'({X[i]:.2f}, {y[i]:.2f})', fontsize=8, alpha=0.5)

    # 添加标题和标签
    plt.title('词汇指数与其对应得分拟合曲线')
    plt.xlabel('词汇指数')
    plt.ylabel('词汇得分')
    plt.legend()

    plt.show()


def plot_gram():
    dl_sample = pd.read_csv(r"D:\gs\distance_analysis\aes\dataset\ELLIPSE-Corpus\dl_sample.csv")
    dl_sample['g_error'] = dl_sample['full_text'].progress_apply(lambda x: check_grammar_errors(x))

    query = """select Grammar, g_error from dl_sample"""

    res = sqldf(query=query, env=locals())

    popt, pcov = curve_fit(model_func_exp, res['g_error'].values, res['Grammar'].values)

    a, b, c = popt

    X = dl_sample['g_error'].values
    y = dl_sample['Grammar'].values

    # 生成拟合曲线的 x 值
    x_fit = np.linspace(min(X), max(X), 100)
    y_fit = model_func_exp(x_fit, a, b, c)

    # 绘制原始数据点
    plt.scatter(X, y, label='源数据', color='blue', alpha=0.6)

    # 绘制拟合曲线
    plt.plot(x_fit, y_fit, label='拟合曲线', color='red')

    # 标注拟合的点
    for i in range(len(X)):
        plt.text(X[i], y[i], f'({X[i]:.2f}, {y[i]:.2f})', fontsize=8, alpha=0.5)

    # 添加标题和标签
    plt.title('语法错误个数与其对应得分拟合曲线')
    plt.xlabel('语法错误个数')
    plt.ylabel('语法得分')
    plt.legend()

    plt.show()


if __name__ == '__main__':
    plot_gram()
