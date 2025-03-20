import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


def preprocess_text(text):
    # 分词
    tokens = word_tokenize(text)
    # 停用词过滤
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
    # 词形还原
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    return lemmatized_tokens


# 计算词汇密度（Lexical Density）
def calculate_lexical_density(tokens):
    # 实词是名词、动词、形容词和副词，这里简单地假设所有词都是实词
    # 在实际应用中，可能需要更复杂的词性标注
    lexical_density = len(tokens) / len(tokens) * 100
    return lexical_density


# 计算词汇多样性（TTR）
def calculate_ttr(tokens):
    unique_words = len(set(tokens))
    total_words = len(tokens)
    ttr = unique_words / total_words
    return ttr


# 计算标准化形符比（STTR）
def calculate_sttr(tokens):
    unique_words = len(set(tokens))
    total_words = len(tokens)
    sttr = unique_words / np.sqrt(total_words)
    return sttr


# 计算形态复杂度加权
def calculate_morphological_complexity(tokens):
    complexity_weight = 0
    for token in tokens:
        if len(token) >= 8:
            complexity_weight += 1.5
        else:
            complexity_weight += 1
    return complexity_weight


# 特征提取函数
def extract_features(text):
    tokens = preprocess_text(text)
    ld = calculate_lexical_density(tokens)
    ttr = calculate_ttr(tokens)
    sttr = calculate_sttr(tokens)
    morphological_complexity = calculate_morphological_complexity(tokens)
    return [ttr, ld ** 2, morphological_complexity]


# 示例数据
# 假设您有9篇样例文章，每篇文章有一个复杂度评分（1-5分，0.5分间隔）
df = pd.read_csv(r"D:\gs\distance_analysis\aes\dataset\ELLIPSE-Corpus\dl_sample.csv")


sample_texts = df['full_text'].values
sample_scores = df['Vocabulary'].values

print(sample_texts)

print(sample_scores)
# 提取特征并准备训练数据
X = []
y = []
for text, score in zip(sample_texts, sample_scores):
    features = extract_features(text)
    X.append(features)
    y.append(score)

# 转换为NumPy数组
X = np.array(X)
y = np.array(y)

# 构建二阶多项式回归模型
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

model = LinearRegression()
model.fit(X_poly, y)

# 打印模型参数
print("模型参数:")
print("截距 β0:", model.intercept_)
print("系数 β1, β2, β3:", model.coef_)


def check_vab_score(test_text):
    test_features = extract_features(test_text)
    test_features_poly = poly.transform([test_features])
    predicted_score = model.predict(test_features_poly)[0]

    print(f"测试文本的综合词汇复杂度指数: {predicted_score:.2f}")

for x in sample_texts:
    check_vab_score(x)
