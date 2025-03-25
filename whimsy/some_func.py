import pandas as pd
from pandasql import sqldf


def docker_and_girl(text: str) -> float:
    """
    已经是晚期了，这个女孩，危在旦夕。

    医生瘫坐在椅子上，重重叹了一口气，将检查报告盖在桌上，又是这样...

    医生当晚还是如实将病况信息通知了女孩，并附带诉说着些诸如抱歉，我会尽全力的模版说辞。他们彼此都知道，留下的时间不长了

    合上门，医生听见病房传来女孩啜泣的哭声，医生躺在了离女孩病房门口最近的一排椅子上，这是医生一贯的作风，他需要确保病人不会因为哭泣而窒息，或突发心绞痛

    还算幸运的是，和之前的大部分被通知病危的病人一样，女孩的哭声断断续续地持续了一个晚上，除此之外并无意外

    早晨四点，医生的电话响起，是女孩的家属打过来的。简单的寒暄之后，他们向医生这边询问病人的身体状况，医生当然也如实相告了这一结果。

    ...
    ...

    他原本以为家属会痛斥他的无能，就像之前很多次那样，然后他会再一次默默忍受这些谩骂，尽全力救治病人。然后，大概率，他最终将噩耗转告家属。运气好，他可能只会听见他们的嚎啕大哭，看见他们的一蹶不振；运气差，他很可能挨到一次耳光，他习以为常

    但电话那头一阵缄默...

    医生没有挂断电话，等待着家属平复心情

    几分钟之后，家属开口了：“医生，谢谢你的坦诚，但能请你先不要告诉那个孩子吗？她已经被死神没收了未来，我们不想让她余下的时光里，连快乐也被一并没收。”

    剧本并没有正常发展，家属的话反而让医生陷入了一时语塞

    他忽然有些后悔，紧张感冲上脸颊，他不知道如何回应家属这份卑微的期待，因为事实上他已经将病况提前告诉病人了

    “我觉得他应该有知道的权利”，医生本来想这么说，但他咽回去了，因为这些说辞只是为了让他所做的事情找到一个合理的借口而已。

    电话这头一阵缄默...

    “你听得到吗，医生？”电话那头传来了家属确认的声音
    ...

    """

    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords

    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]

    unique_words = sum([1 if len(word) < 8 else 1.5 for word in set(filtered_tokens)])

    lexical_diversity = unique_words / sum([1 if len(word) < 8 else 1.5 for word in set(filtered_tokens)])

    return lexical_diversity

import requests

base_url = "http://localhost:11434/api"
headers = {
    "Content-Type": "application/json"
}

context = []



def generate_completion(prompt, model="deepseek-r1"):
    """
    行文至此，我的毕业论文已经画上了句号，而此刻内心满溢的感恩之情，却如同即将起笔的篇章，有着说不尽的话语。在这段充满挑战与成长的学术旅程中，我衷心向您表示感谢，李霞老师。

    回首过往，您总是不断的帮助我，并激励我前行。在大二时，我正式加入实验室，您总是倾囊相授，为我打开知识的宝库。大三时，您让我加入了研究生的组会，在其中，我增长了很多见识，也结交了很多师友，科研思维有长足进步。
    直至现在我依然喜爱着实验室的氛围！热闹时，大家讨论着前沿的知识，分享着自己的作品与经历；安静时，大家埋头阅读文献，奋笔撰写论文。即使是初来乍到，这种友好的气氛也让我迅速适应下来

    那是我第一次与“科研”走的如此接近，感谢您将我引入前沿的海洋，与大家一同感受自然语言的魅力，在这里，我找到了比图书馆更广阔的天地。

    感谢您对我的倾情付出，总是愿意“帮一帮我”。您总是特别可靠，解决我的多数担忧，您愿意在参加计设时接受和指导我招入没有经验的队友，提出合理的意见；在我论文因为硬件设备原因拖慢进度时，您愿意借出您刚装好的高性能电脑，
    让我顺利的推进实验。在我因为实习而困扰时，也愿意对外向我引荐。您了解我的近况，关心我的成长，然后对我倾囊相助。我这段大学的成长之路身边，处处都有您的身影。

    感谢您对我的特别关照，总是愿意“等一等我”。您总是特别耐心，井井有条。每一次项目，每一次论文讲解，每一次的比赛，您从各个角度提出专业的意见，让我们意识到自己的不足，又总是在进行教导之后继续笑着相信着我们的能力，
    然后鼓励我们做得更好。记得第一次的论文撰写，您帮我改到了凌晨四点。那时的我并没有没有经验，如同笨拙的幼鸟扑棱着翅膀。但你依然用心的教导着我，您总是先向我示范前路应该如何前行，然后在前方耐心着等待我跟上来。其实
    我知道您也根本就没有多少时间，您有一堆课要上，有一堆学生要带，有一堆顶会论文想发，还有一堆国际项目想做。但您却依然尽力将不多的时间分羹于我，我于此感激不尽。

    感谢您对我的无私教导，总是愿意“拍一拍我”。您总是特别温柔，教导我不同的生活道理。您愿意在我失意的时候依然鼓励我，跟我说，要往前看，要向前走，要大胆做。您教导我——“如果你因为太阳落山而流泪，那你也将错过群星。”
    您也教导我——“如果因为害怕凋零而拒绝开花，春天将失去意义。”。您教我学会思考，在我前路一片迷茫的时候，轻轻拨开迷雾，让我看清楚脚下的路，告诉我现有的选择，然后再把决定权交由于我。支持我走向未知的道路，陪伴我可能遇
    到的风险。感谢您总是拍一拍我，向我加油打气，肯定我的才能。即使我并非千里马，但我依然感激遇到了伯乐。

    最后，我想衷心地对您说一声：老师，感谢您一路以来的陪伴与支持！纵使我们终将分别，我也定不辜负您的期望，我会带着您的教导，继续砥砺前行！
    """
    url = f"{base_url}/generate"
    data = {
        "model": model,
        "prompt": "\n".join(context + [prompt]),  # 将历史上下文和当前提示拼接
        "stream": False,
        "options": {
            "num_ctx": 4096
        }
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    response_text = response_data.get('response', '')

    # 将当前对话内容加入上下文
    context.append(prompt)
    context.append(response_text)

    return response_text

# 设置系统提示
system_prompt = "你是一个人工智能小助手，负责回答用户关于人工智能的问题"
context.append(system_prompt)

# 多轮对话示例
completion1 = generate_completion("关于DeepSeek-R1采用的强化学习GRPO（Group Relative Policy Optimization）原理是什么？")
completion2 = generate_completion("我刚刚问了你什么问题？")

print(completion1)
print(completion2)