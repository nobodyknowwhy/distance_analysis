import random

import nltk
import numpy as np
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize


def get_synonyms(word, pos=None):
    """获取单词的同义词"""
    synonyms = set()
    for syn in wordnet.synsets(word, pos=pos):
        for lemma in syn.lemmas():
            synonym = lemma.name().replace("_", " ").lower()
            if synonym != word:
                synonyms.add(synonym)
    return list(synonyms)


def synonym_replacement(words, n=2):
    """同义词替换"""
    new_words = words.copy()
    random_word_list = list(set([word for word in words if word not in ['.', ',', '!', '?']]))
    random.shuffle(random_word_list)
    num_replaced = 0

    for random_word in random_word_list:
        # 获取词性标签
        pos = nltk.pos_tag([random_word])[0][1][0].lower()
        pos = pos if pos in ['a', 'r', 'n', 'v'] else None

        synonyms = get_synonyms(random_word, pos)
        if len(synonyms) >= 1:
            synonym = random.choice(synonyms)
            new_words = [synonym if word == random_word else word for word in new_words]
            num_replaced += 1

        if num_replaced >= n:
            break

    return ' '.join(new_words)


def random_insertion(words, n=2):
    """随机插入"""
    new_words = words.copy()
    for _ in range(n):
        add_word(new_words)
    return ' '.join(new_words)


def add_word(new_words):
    """插入单个同义词"""
    synonyms = []
    counter = 0
    while len(synonyms) < 1:
        random_word = new_words[random.randint(0, len(new_words) - 1)]
        pos = nltk.pos_tag([random_word])[0][1][0].lower()
        pos = pos if pos in ['a', 'r', 'n', 'v'] else None
        synonyms = get_synonyms(random_word, pos)
        counter += 1
        if counter >= 10:
            return
    synonym = random.choice(synonyms)
    new_words.insert(random.randint(0, len(new_words) - 1), synonym)


def random_swap(words, n=2):
    """随机交换"""
    new_words = words.copy()
    for _ in range(n):
        swap_word(new_words)
    return ' '.join(new_words)


def swap_word(new_words):
    if len(new_words) >= 2:
        idx1, idx2 = random.sample(range(len(new_words)), 2)
        new_words[idx1], new_words[idx2] = new_words[idx2], new_words[idx1]


def random_deletion(words, p=0.2):
    """随机删除"""
    if len(words) == 1:
        return words

    new_words = []
    for word in words:
        if random.random() > p:
            new_words.append(word)

    if len(new_words) == 0:
        return ' '.join(words[random.randint(0, len(words) - 1)])

    return ' '.join(new_words)


def eda(sentence, alpha_sr=0.1, alpha_ri=0.1, alpha_rs=0.1, p_rd=0.1, num_aug=20):
    """执行EDA增强"""
    words = word_tokenize(sentence)
    num_words = len(words)

    augmented_sentences = []
    num_new_per_technique = num_aug // 4 + 1

    # 同义词替换
    if alpha_sr > 0:
        n_sr = max(1, int(alpha_sr * num_words))
        for _ in range(num_new_per_technique):
            a_words = synonym_replacement(words, n_sr)
            augmented_sentences.append(a_words)

    # 随机插入
    if alpha_ri > 0:
        n_ri = max(1, int(alpha_ri * num_words))
        for _ in range(num_new_per_technique):
            a_words = random_insertion(words, n_ri)
            augmented_sentences.append(a_words)

    # 随机交换
    if alpha_rs > 0:
        n_rs = max(1, int(alpha_rs * num_words))
        for _ in range(num_new_per_technique):
            a_words = random_swap(words, n_rs)
            augmented_sentences.append(a_words)

    # 随机删除
    if p_rd > 0:
        for _ in range(num_new_per_technique):
            a_words = random_deletion(words, p_rd)
            augmented_sentences.append(a_words)

    # 去重并截取指定数量
    augmented_sentences = [sentence for sentence in augmented_sentences if sentence != ' '.join(words)]
    augmented_sentences = list(set(augmented_sentences))
    random.shuffle(augmented_sentences)

    return augmented_sentences[:num_aug]


if __name__ == "__main__":
    original_text = "The quick brown fox jumps over the lazy dog. It's amazing to see such a beautiful scene in nature."

    # augmented_texts = eda(original_text, num_aug=20)

    import pandas as pd

    df = pd.read_csv(r"D:\gs\distance_analysis\aes\dataset\ELLIPSE-Corpus\dl_sample.csv")
    content_to_df = {'text':[], 'score':[]}

    for index, row in df.iterrows():
        augmented_texts = eda(row['full_text'], num_aug=25)
        for text in augmented_texts:
            content_to_df['text'].append(text)
            content_to_df['score'].append(np.floor(row['Overall']))

    df_tar = pd.DataFrame(content_to_df)

    df_tar.to_csv(r"D:\gs\distance_analysis\aes\out\second_clean\test\aes_eda.csv", index=False)
    print(df_tar)