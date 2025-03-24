import pandas as pd
from pandasql import sqldf


def docker_and_girl(text: str) -> float:
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
