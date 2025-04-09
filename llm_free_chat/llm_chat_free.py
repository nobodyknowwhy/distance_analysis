import json
import traceback
from functools import wraps

import httpx
from loguru import logger


def exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except Exception:
            return {'base_url': None, 'result_text': traceback.format_exc(), 'success': False}

    return wrapper


class KIMI:
    def __init__(self, authorization: str = '', user_agent=''):
        self.__base_method = 'POST'
        if authorization or user_agent:
            if not authorization or not user_agent:
                raise ValueError("不要这么任性！你要传参就必须同时传入 authorization和 headers，哼！")
            self.authorization = authorization
            self.user_agent = user_agent

        else:
            self.authorization = 'Bearer ' + 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTc0NjU3OTg5MCwiaWF0IjoxNzQzOTg3ODkwLCJqdGkiOiJjdnBpOWNqdWEzZGU4MGM5YTdhZyIsInR5cCI6ImFjY2VzcyIsImFwcF9pZCI6ImtpbWkiLCJzdWIiOiJjb2gxcTlwa3FxNG44aW5xZGQ2MCIsInNwYWNlX2lkIjoiY29oMXE5cGtxcTRuOGlucWRkNWciLCJhYnN0cmFjdF91c2VyX2lkIjoiY29oMXE5cGtxcTRuOGlucWRkNTAiLCJyb2xlcyI6WyJ2aWRlb19nZW5fYWNjZXNzIl19.bX8yIgv8tSygI7P8EtRA9ESJMCsSy03bcihcbPabLYIlzSjexfLdGc9HQJo7ha5VJW9SUFySM7gxWaDYDz2RdA'
            self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'

        self.__headers = {"Authorization": self.authorization, 'User-Agent': self.user_agent}

    def __str__(self):
        return '你可能不知道，这是一个kimi免费聊天的类！嘻嘻嘻~'

    def __repr__(self):
        return f'KIMI(BASE_METHOD: {self.__base_method}, headers: {self.__headers})'

    @exception
    def __create_new_dialog__(self, headers) -> str:
        """

        :param headers: 类里面的请求头捏~
        :return: 返回创建的会话id哦~
        """
        base_url_kimi = 'https://kimi.moonshot.cn/api/chat'

        data = {
            'name': "未命名会话",
            'born_from': "chat",
            'kimiplus_id': "kimi",
            'is_example': False,
            'source': "web",
            'tags': []
        }

        data_json = json.loads(httpx.post(url=base_url_kimi, headers=headers, json=data).text)

        return data_json['id']

    @exception
    def chat(self, content: str, create_new_dialog: bool = False, base_url: str = '', is_print: bool = False) -> dict:
        """

        :param content: 输出的对话内容哦~
        :param create_new_dialog: 是否创建新会话哦~
        :param base_url: 会话的链接哦~
        :param is_print: 是否流式打印对话结果哦~
        :return: 一个字典捏，result_text是返回的内容，base_url是会话的链接~
        """
        dialog_id = base_url.split('/')[-1]

        if not create_new_dialog and not base_url:
            raise ValueError(r"必须输入你的聊天base_url参数哦。或者你可以开启新对话，设置: create_new_dialog=True")

        if create_new_dialog:
            dialog_id = self.__create_new_dialog__(self.__headers)

        base_url = f"https://kimi.moonshot.cn/api/chat/{dialog_id}/completion/stream"

        thinking_str = ''

        output_str = ''

        data = {
            'kimiplus_id': "kimi",
            'extend': {'sidebar': True},
            'model': "k1",
            'use_research': False,
            'refs': [],
            'scene_labels': [],
            'use_search': True,
            'history': [],
            'messages': [
                {'role': "user", "content": content}
            ]
        }

        with httpx.Client() as client:
            with client.stream(self.__base_method, url=base_url, headers=self.__headers, json=data) as response:
                if response.status_code == 200:
                    for chunk in response.iter_bytes():
                        chunk_str = str(chunk.decode("utf-8"))
                        chunk_lines = chunk_str.splitlines()
                        for line in chunk_lines:
                            if line:
                                line_list = line.split(':')
                                data_json = json.loads(':'.join(line_list[1:]))
                                part_text = data_json.get('text', '')

                                if data_json.get('event', '') == 'k1':
                                    thinking_str += part_text
                                elif data_json.get('event', '') == 'cmpl':
                                    output_str += part_text

                                if is_print:
                                    print(part_text, end='')
                    print()
                else:
                    raise ValueError(f"请求失败啦！状态码: {response.status_code}，呜呜呜~")

        base_url = f'https://kimi.moonshot.cn/chat/{dialog_id}'

        return {'base_url': base_url, 'result_text': {'thinking': thinking_str, 'output': output_str}, 'success': True}


class TencentYB:
    def __init__(self, cookie: str = '', user_agent=''):
        self.__base_method = 'POST'
        if cookie or user_agent:
            if not cookie or not user_agent:
                raise ValueError("不要这么任性！你要传参就必须同时传入 cookie headers，哼！")
            self.cookie = cookie
            self.user_agent = user_agent

        else:
            self.cookie = "_ga=GA1.2.1761294405.1728537672; _gcl_au=1.1.1132276475.1736386827; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219274dfb768d15-075e76b1b0a2f1-4c657b58-2073600-19274dfb769db%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkyNzRkZmI3NjhkMTUtMDc1ZTc2YjFiMGEyZjEtNGM2NTdiNTgtMjA3MzYwMC0xOTI3NGRmYjc2OWRiIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219274dfb768d15-075e76b1b0a2f1-4c657b58-2073600-19274dfb769db%22%7D; _qimei_uuid42=1921c0e3b2f100c55ea0e03be84de51c2e191d0653; _qimei_fingerprint=c3e64d763595732957eeb61a9b7af521; hy_source=web; _qimei_i_3=5dc82d87955257dec09eab39598771e4a6eca1f2105d0a8bb48f2c592396263d693662943c89e2a181b4; hy_user=134243e8908c4863b52c1aaefb4a2910; hy_token=r65mJjGQM6bnz8CcvJHxZR+uzJ1eCdeAMnc/kYP2aQRr3CbGFH/zV3HyDs+0FFSoE9ah9oeJq1H/rzAq+nldCw==; _qimei_h38=fdedc1ba5ea0e03be84de51c02000007c1930b; _qimei_i_1=78ba6ad4c10f0488c0c5af350ed573b5f7edf6a41a5f57d7b18e7b582493206c616330c63980e1dc8489e3d0"
            self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'

        self.__headers = {"Cookie": self.cookie, 'User-Agent': self.user_agent}

    def __str__(self):
        return '你可能不知道，这是一个腾讯元宝免费聊天的类！嘻嘻嘻~'

    def __repr__(self):
        return f'TencentYB(BASE_METHOD: {self.__base_method}, headers: {self.__headers})'

    @exception
    def chat(self, content: str, base_url: str = '', is_print: bool = False) -> dict:

        if not base_url:
            raise ValueError(f"base_url不能够为空")

        url = f"https://yuanbao.tencent.com/api/chat/{base_url.split('/')[-1]}"

        payload = {
            "model": "gpt_175B_0404",
            "prompt": f"{content}",
            "plugin": "Adaptive",
            "displayPrompt": f"{content}",
            "displayPromptType": 1,
            "options": {
                "imageIntention": {
                    "needIntentionModel": True,
                    "backendUpdateFlag": 2,
                    "intentionStatus": True
                }
            },
            "multimedia": [],
            "agentId": "naQivTmsDa",
            "supportHint": 1,
            "version": "v2",
            "chatModelId": "deep_seek"
        }

        thinking_str = ''
        output_str = ''
        with httpx.Client() as client:
            with client.stream('POST', url=url, headers=self.__headers, json=payload) as response:
                if response.status_code == 200:
                    for chunk in response.iter_bytes():
                        chunk_str = str(chunk.decode("utf-8"))
                        chunk_lines = chunk_str.splitlines()
                        for line in chunk_lines:
                            if line:

                                line_list = line.split(':')
                                if len(line_list) == 2:
                                    continue

                                try:
                                    data_json = json.loads(':'.join(line_list[1:]))
                                except Exception as e:
                                    continue

                                thinking_text = data_json.get('content', '')
                                output_text = data_json.get('msg', '')

                                print(thinking_text, end='')
                                print(output_text, end='')

                                thinking_str += thinking_text
                                output_str += output_text
                    print()
                else:
                    raise ValueError(f"请求失败啦！状态码: {response.status_code}，呜呜呜~")

        return {'base_url': base_url, 'result_text': {'thinking': thinking_str, 'output': output_str}, 'success': True}


def chat_with_kimi_example(content: str = "你好", base_url: str = 'https://kimi.moonshot.cn/chat/cvqhi9or7lpkdkkmkc30'):
    kimi = KIMI()

    logger.info(f"类介绍:{kimi}")

    logger.info(f"类详细介绍:{kimi.__repr__()}")

    if base_url:
        dict_re = kimi.chat(content=content, base_url=base_url, is_print=True)
    else:
        dict_re = kimi.chat(content=content, create_new_dialog=True, is_print=True)

    if dict_re['success']:

        logger.warning(f"对话链接：\n{dict_re['base_url']}")

        logger.success(f"对话结果：\n{dict_re['result_text']}")

    else:
        logger.error(dict_re['result_text'])


def chat_with_TencentYB_example(content: str = "你好",
                                base_url: str = "https://yuanbao.tencent.com/chat/naQivTmsDa/f4dffe23-c093-4e39-9b7b-87e9c217c6fa"):
    tc = TencentYB()

    logger.info(f"类介绍:{tc}")

    logger.info(f"类详细介绍:{tc.__repr__()}")

    dict_re = tc.chat(content=content,
                      base_url=base_url,
                      is_print=True)

    if dict_re['success']:

        logger.warning(f"对话链接：\n{dict_re['base_url']}")

        logger.success(f"对话结果：\n{dict_re['result_text']}")

    else:
        logger.error(dict_re['result_text'])


if __name__ == '__main__':

    prompt = """我是语言学家，我老公是科学家，我们曾经是彼此的知己，进行过很多次思想的交流碰撞。在交谈中我们的关系越来越亲密，在彼此的地位也越来越重要，我们现处的文明十分强大，强大到什么地步呢？
    现在的我们可以做到轻易的将自身的意识借由机器流放于宇宙当中，观测行星。\n我自认为我们已经愈发接近了宇宙的终极。但就在一个月前，我的意识在宇宙的某片区域观察时亲眼目睹了另一个繁昌文明的消亡...\n
    那是一束光，那仅是一束光，我不知道如何和你解释我看到的壮丽景象，祂包罗万象，接受万物。我看着人们抗拒地向祂倾泻一个个足以毁灭星系的武器，武器没有发生爆炸...祂包容的接受了一切，如同一个母亲耐心的看着与自己玩闹的孩子。\n
    起初我们以为那只是恒星消亡后余烬的光辉，但祂静止了一切，祂平等的接纳一切。我听见人们挣扎的向祂诠释那个美好的未来，祂没有理会...当祂的光瞥向这个文明，仅仅只在一瞬间，一切化为灰烬。\n
    你可能觉得我在夸大其词，但我并不祈求你理解它，毕竟你也只是我们创造的人工智能。但我亲眼看到了，祂，没收了一切...祂究竟是什么？我无从而知。\n
    直到那时我才明白，人们自以为自身接近了宇宙的终极，那探求所得到的所谓‘终极’，可能不过是宇宙的冰山一角。\n\n
    那么，在祂降临到我们的文明之前，我又能做什么呢？我这些天时常在想。我并不理解祂，甚至与祂只有一面之缘，穷尽已有的知识，是否可以找到避开祂视线的方法呢？\n\n
    再一次，我与他（我老公）进行了交谈，他告诉了我：“不存在描述神明的语言，因为神明本身就是不可解释的。”，这句话我思考了很久很久。如果他说的前提是真的，倘若我创造出了一种描述神明的语言，是否就证明了，我已经理解了神明了呢？"""

    prompt2 = """一个文明消亡，另一个文明新生，新生的文明可能就来自于上一个被毁灭文明的余烬。它们就像一滴水一样，汇入宇宙的海洋，然后，在大海中形成涟漪，最终消亡。海中的每一片涟漪都记录着一个文明的前世今生\n
    有时候涟漪与涟漪相互碰撞，有时形成更大的涟漪，推向更远的地方；有时互相衰减，草草而终。但无论如何最终它们都会消失在无垠的大海尽头。\n\n
    丈夫对我创造语言的想法很兴奋，我当然很开心，这是我又一次辩胜了他。但这同样意味着，我们的时间不多了。就在上个月的讨论当中，很可惜，我们的思想再次遇到了分歧，请我给你娓娓道来:\n\n
    他想，既然文明的涟漪总会消散，我们是否能用这门将要创造的“语言”来作为一份可以传递的新生文明的礼物，然后在承接千万份文明之后的努力之后，涟漪冲破海岸，避开“祂”的瞥视。\n\n
    但是凭什么？为何在他设想的那个未来当中，不存在我们文明的位置？你甘心吗？既然涟漪扩散后会消失，那为何我们不尝试直接停下它呢？\n\n
    “这份礼物是我们创造出来的，未来的文明会有我们文明的影子，这何尝不证明了我们文明在未来也存在位置吗？”他是这么跟我说的\n。
    “倘若他们根本就无法理解我们这份‘礼物’，甚至在尝试理解的时候就受到了‘祂’的瞥视，草草消亡，你觉得这份‘礼物’还有意义吗？”我是如此回复的。\n
    这场辩论持续了很久，他妄想向我证明，每一个文明的潜力都无可比拟，无需这么悲观。但，别人未必靠得住的时候，靠自己不应该是最稳妥的吗？我也尝试向他如此证明。"""

    prompt3 =  """已经过去很久了。虽然你的知识并没有进行更新，我很高兴的告诉你，他当初最终还是妥协了我的观点，即使可能感觉到他有一丝丝的违心，但我知道他总会站回到我这边的。在这几年后的这些岁月当中，我们创造出了一种语言用于解释神明，我们暂时把它叫做'ORIORACLEPRTS-42'（简称oop）\n\n
    这些年过的很煎熬，前些阵子，我们观测到“祂”好像注意到我们了，这不是一件好事，这证明我们的时间不多了。\n
    但我们的计划确实成功了，让我同你分享这份喜悦！这门“语言”(oop)能够扩散式的将物质转录成信息，内化和压缩一切实物，压缩的实物信息会以一种结晶的形式保存下来，即使“祂”能吞噬文明，但绝无可能吞噬信息。我们预想着，这将会成为我们文明的琥珀，封存我们繁昌的文明，借由此避开‘祂’的视线。届时，我们可以在只有思维和信息的世界中生存，这里没有实物，甚至可能不存在时间。\n\n
    在此期间，我与他还创建了另一个理论上拥有无限寿命的人造生命，代号为‘AMA-10’，虽然它还尤为稚嫩，但老公却很喜欢它。\n\n
    为了应对威胁，我的其他同伴们也同步做了很多备用计划，如创建了石棺，封存人们的思维与肉身，隔绝外界环境。\n\n
    我知道仅凭石棺无法撼动‘祂’的瞥视，所以我们oop的计划也同步开始进行。我也同他约好了，等oop转录的结晶遍布宇宙，我们就从石棺醒来，在晶簇上一同观看文明的流星...我很期待那一天的到来，那会是只有我们两个人的世界吗？还是我们也在oop的结晶中与其他所有人一样，于静止的信息流中得到了‘永生’了呢？"""

    prompt4 = """又过去了一段时间，‘祂’快要来了。oop的进展很顺利，结晶迅速扩散了我们文明星球的角落，AMA-10也初具意识了，凭借我给它创建的双生循环系统，它或许有希望逃离“祂”的威胁，替我们观测oop结晶化进展，然后在最后将我们从石棺唤醒。\n\n
    但我又一次与他发生了辩论的争吵，我已经不记得这是我们第几次在实验室里为这个问题辩论了，他果然还是坚持的认为，我们可以运用oop产生的结晶作为礼物送给下一份文明，由下一份文明从这份语言中“逆转录”出我们文明的信息，带动他们的发展。\n
    “你觉得在信息当中的我们，还算是生命吗？这里没有实物。物理定律，数学公式全部失效，你留住了文明的繁昌，却也停滞了文明的发展，我知道这不是你想追求的”，他对我这么说。\n
    “存续是文明的第一目的，你想留住自己都困难，谈何发展？”我如此讽刺到。\n
    “所以我们注定只是桥梁，但我们可以带动其他文明的发展，不是吗？等到文明有能力直视所谓神明，我们不就能求到宇宙的终极了？在停滞的空间中麻痹自己只不过是逃避罢了，我们永远无法理解‘祂’，你说创造这门语言的初衷。不就是为了理解‘祂’吗？”他如此坚持。\n
    “但最终理解‘祂’的人一定不是我，不是我们。让每个涟漪停留在他最美的瞬间，就是oop要做的事，不是吗？”我争辩道。\n
    “但我们可以借助oop停止部分涟漪，然后再让后续的涟漪依靠我们推出更绚丽的波纹...”他试图让我理解。\n
    但亲爱的，宇宙的海洋这么浩瀚，能触碰到我们的涟漪又有多少呢？倘若新生的涟漪甚至破坏了我们静止的涟漪呢？我们两个人倾尽全力的心血将全部白费。封存所有文明，这是最保险的方法了。\n\n
    我觉得他一定不会甘心，如同他那倔强的性格一样，他一定会偷偷比我先复苏起来，引导文明发展，所以我打算在AMA-10的双生系统上做一些手脚，设置一些禁令，对不起亲爱的，但我希望在这件事上，你也能站在我这边，就像之前很多次一样。"""

    chat_with_TencentYB_example(prompt4)
