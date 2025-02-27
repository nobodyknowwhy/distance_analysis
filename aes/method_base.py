"""
为了能够使得机器能够生成对应文本的文章，按照给定的评分要求来生成对应文本的文章，我们倡导机器可以适当有一些语法错误，适当句子不连贯，从而来适应评分
的标准。以下设计的所有函数都采用内部导包的方式来进行，确保函数只有在用到的时候才下载对应的包资源
"""

"""
Dataset: ASAP/ AES++
prompt1: Write a letter to the editor of a newspaper about how computers affect society today.
prompt2: Write a letter to the editor of a newspaper about censorship in libraries
prompt3: Write a review about an article called Rough Rough Road by Joe Kurmaskie. The article will be provided.
prompt4: Explain why the author concludes the story the way the author did. The short story will be provided.
prompt5: Describe the mood created by the author in the memoir. Support your answer with relevant and specific information from the memoir.
prompt6: Describe the difficulties that builders of the Empire State Building faced because of allowing dirigibles to dock there.


Dataset: EELLIPSE


假设我们现在有若干篇共包含7主题的文章，文章的评分标准是1-5分，假设每一种文章（评分 | 主题）都有两篇，即现在一共70篇文章现在打算想让LLM根据特定的
评分标准生成对应评分的文章，从而扩充数据集。由于LLM生成的文章并不一定都完美符合评分标准给定的分数（比如叫LLM生成3分的文章，LLM可能生成的过于完美，
实际生成了6分的文章），因此对生成数据的筛选显得很重要。现在，由于数据集不够，我们无法构建一个准确的评分模型进行测试，同时我也并不想要对生成的机器文
本进行人工标注，因为我研究的目的就是解决数据量不够，或人手缺失的问题。所以我究竟有什么手段知道LLM实际生成的文章是否符合对应的分数呢？

初步有了一些想法，但是并不确定。假设评分标准是 \{standard[1-5]}，分别代表了1-5的评分标准

对于分数越低的文章，我们可以知道，语法错误会越多，文章会越不连贯，可读性差，同时还有一种可能就是，文章没有紧扣主题，偏离了主旨，对于满分的文章，我们
可以知道，评分标准如下：
VG:No lexical or grammatical errors, extensive use of a wide range of vocabulary, and the ability to flexibly use a variety of sentence patterns;
LF:Fluent and coherent expression with natura transitions and well-organized content structure;
EA:Fully consistent with the topic and able to convey rich information effectively.

对于只有1分的文章，评分标准则是：
VG:Numerous vocabulary and grammatical errors seriously impair comprehension,or a low word count reflects only simple use of words and basic sentence patterns;
LF:Chaotic expressions with multiple inconsistencies;
EA:Expression is generally in line with the topic.but it isn't easy to understand in a few places.

对于输入进LLM的提示词prompt，我们可以根据对应的评分标准进行输入，比如：
now you are required to generate a text fixed the score \{score[x]}, with the essay's topic \{topic[x]}. In order for 
the article you generate to qualify for the corresponding score, the essay you generated need to have the following 
requirements: \{standard[x]} -- [\{cite_1}], sometimes you can make a few mistakes to suit the target requirements.

在上述的LLM的prompt当中，我们规定了机器需要按照特定的主题和对应分数的评分标准生成对应的文章，这样可以避免大部分的数据量预期偏差问题。

对于生成的文章，我们需要进行质量检测，即数据蒸馏。一开始我打算将其分成两种蒸馏方式：1. 拟人度蒸馏， 2. 生成文章符合评分标准的准确度蒸馏

拟人度蒸馏，顾名思义即是对生成的文本进行检测，查看它是否近似于人类语言，但是后面觉得并不妥当，所以我进行了删除，理由如下：
1. 一开始我打算采用之前研究项目所产生的模型（即区别LLM和人类文本的模型 -- [\{cite_2}]）来筛选出对应的对抗样本，具体做法如下：
      -- LLM生成文本
      -- 放如区别模型（[\{cite_2}]）当中进行相关的检测
      -- 若检测发现并不符合对应要求，模型分辨出是机器生成文本，则重新生成；若文本成功绕过了模型的检测，则保留
    由于模型[\{cite_2}]的准确率决定了此LLM注定要生成巨大规模的文本才可能有少量的数据集产出，因此效率极低，也不适合真正投放入实践当中，因此考虑再
    三将此方法废除
    
2. 后来我又想到了另外一种方法，是否能直接微调LLM，使其专门按照区别模型的反方向生成对抗文本呢？对应的具体做法如下
      -- LLM生成文本
      -- 放如区别模型（[\{cite_2}]）当中进行相关的检测
      -- 根据模型的区别效果记录损失，更新LLM权重，直至此LLM生成的文本模型大抵区别不出来，此刻可以认为此模型生成的文本近似都是人类文本
    但由于微调需要的设备要求较高，且技术难度较大，从此模型到结果模型的过程需要的时间也十分漫长，而且不同的LLM得到的训练结果也不尽相同，真放到现实
    应用当中实用性也不高因此也放弃了此方法

3. 最后我想着，其实模型重点在于能够准确对人类生成文本进行打分，区别是否是人类生成的其实并没有这么重要，所以综合考虑将拟人度蒸馏删除

接下来就是准确度蒸馏，我需要解决以下两个问题
1. LLM根据对应prompt [\{cite_1}] 生成的文章并不一定就符合打分的评分标准，我需要如何检查？
2. 如果LLM生成的文章已经检查过确实不符合标准了，重新生成的时候要对新的prompt做哪些改动？

我们慢慢来，首先对于问题一，我们可以根据评分标准出发，构建一个基于规则，或基于模型的简单检测器，对机器生成的文本进行检查，查看其生成的文章是否符合标
准，需要注意的是，我说的检查器并不指的是评分模型，由于我们现在只有70篇文章（每个主题10篇，每个评分14篇，每个特定主题特定评分2篇），直接构建评分模型
会导致误差过于严重，影响生成文本的结果，所以推出了“检查器”

为了解决这个问题，我们需要先回顾一下评分标准，我们可以知道，评分标准是从VG，LF，EA三个角度出发来对文章进行评分的。
   -- 对于VG而言，其关注到了文章了词汇量，语法错误，词汇错误，句型运用
   -- 对于LF而言，其关注到了文章的连贯性，表达的流畅性，文章的组织结构
   -- 对于EA而言，其关注到了文章与主题的切合程度，表达信息是否丰富
所以我们对于检查器的构建，可以按照以下步骤进行：
   -- 按照VG，LF，EA建立检查函数
   -- 计算出不同的平方在上述构建函数中的分布
   -- 对LLM生成的机器文本内容进行分布检验，查看它是否在合理的分布区间之内
   -- 如果不在分布范围之内，我们认为生成的文本并不符合对应的评分，需要重新生成（ep: 比如需要生成1分的文章，但文章太过流畅，并不在对应分数的分布内
      ，则视为不符合）

但是这样依然会遇到一些问题，因为一篇文章的评分标准是根据VG，LF，EA三个一起决定的，并不是简单的分开决定。例如，一篇低分文章可能VG得分很高，但是剩下
两项LF，EA得分很低，因此造就了低分。这就会导致在分别计算数据函数结果分布时出现很大偏差，为了解决这个问题，我又想到了一些方法。
1. 直接运用简单的机器学习模型解决这个问题，如SVM模型，让模型自动算出这三者的得分会最终造成什么结果
2. 自己设定一个比例值，如VG : LF : EA = 0.4 : 0.3 : 0.3，然后将每个得分加权求和，用最后得出的结果进行决策LLM生成文本的准确性

现在第一个问题已经初步有了思路，现在来看一下第二个问题需要怎么解决，第二个问题是：如果LLM生成的文章已经检查过确实不符合标准了，重新生成的时候要对新
的prompt做哪些改动？
由于重复用相同提示词可能依然会导致得到结果数据的效率低下，所以能够以最小的生成代价生成我们想要的数据也变成了我们的目标之一。因此对于每一次重复生成时
使用的prompt[\{cite_1}]，我们需要在末尾加上一些话语，如：
The essay you generated is not satisfied with the standard \{standard[x]}, please generate again with the topic \{topic[x]}

通过反复强调标准从而引导机器生成的文本更加接近这个标准，同时需要注意的是，为了防止本地运行的模型消耗太多显存，我们最多支持它三次上下文记忆的机会，意
思是，如果机器生成了3次文本依然没有达到目标，会直接情况记忆缓存，释放内存，然后从头开始生成文本。





"""



import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')


def calculate_grammar_error(text: str) -> int:
    """
    这个是一个检查语法的函数，返回的是这一篇文章有多少语法错误，实际上文章越长，语法错误就有可能越多，但是这并不意味着文章越短评分就应该越高，所以
    可能需要考虑返回一个比例值：（有语法错误的句子）/（总句子）所得到的结果。但是这样实际上也会有些问题，因为如果一个句子出现了多处语法错误，证明
    此文章的水平越低，与只出现一处语法错误的句子不应该一视同仁，经过权衡考虑，打算直接返回章语法错误的数量

    :param text: 输入的文本
    :return: 返回文章语法错误的数量
    """
    import language_tool_python
    try:
        tool = language_tool_python.LanguageTool('en-US')  # 对于英语，使用 'en-US'

        matches = tool.check(text)

        print(matches)
        return len(matches)
    except Exception as e:
        print("Error:", e)
        return 0


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
    print(tokens)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]

    total_words = len(filtered_tokens)
    unique_words = len(set(filtered_tokens))

    if total_words == 0:
        return 0.0
    lexical_diversity = unique_words / total_words

    return lexical_diversity


def calculate_avg_sent_len(text: str) -> int:
    """
    一般而言，文章句子越长，代表着文章的复杂度越高，当然这也不一定是绝对的，还需要与句式结构相结合才能评判出文章句子的复杂程度，长句只是复杂句的其
    中一个评判标准，需要注意的是，如果一篇文章某个句子过长，其他句子太短，也会拉高平均句长，过长的句子（总是以', '分割）虽然会使得句子复杂度变高，
    但可能会导致更多的语法错误

    :param text: 输入文章
    :return: 输出文章的平均句长
    """
    from nltk.tokenize import sent_tokenize

    len_sent_list = [len(text_tokenized) for text_tokenized in sent_tokenize(text)]

    return int(sum(len_sent_list) / len(len_sent_list))


def calculate_transition_words(text: str) -> int:
    """
    计算文章中转折词的使用次数。

    :param text: 输入文章
    :return: 返回转折词语的使用次数
    """
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from collections import Counter

    transition_words = {
        "however", "therefore", "moreover", "furthermore", "consequently", "thus", "hence",
        "meanwhile", "subsequently", "additionally", "similarly", "in addition", "in contrast"
    }

    stop_words = set(stopwords.words('english'))

    words = [
        word.lower() for word in word_tokenize(text)
        if word.isalpha() and word.lower() not in stop_words
    ]

    word_counts = Counter(words)
    return sum(word_counts[word] for word in transition_words if word in word_counts)


def check_theme_by_bert(article, theme_description):
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity

    model = SentenceTransformer('all-MiniLM-L6-v2')

    article_embedding = model.encode(article, convert_to_tensor=True)
    theme_embedding = model.encode(theme_description, convert_to_tensor=True)

    similarity = cosine_similarity(article_embedding.reshape(1, -1), theme_embedding.reshape(1, -1))[0][0]

    threshold = 0.7
    return similarity >= threshold, similarity


if __name__ == '__main__':
    import pandas as pd

    df = pd.read_csv('train.csv')
    sample_text = df['full_text'][0]

    print(calculate_avg_sent_len("this is a example with error"))

    article = ''

    theme_description = "A discussion on the future of artificial intelligence and its societal implications."

    result, similarity = check_theme_by_bert(article, theme_description)
    print(f"Article matches theme: {result}")
    print(f"Similarity score: {similarity:.2f}")
