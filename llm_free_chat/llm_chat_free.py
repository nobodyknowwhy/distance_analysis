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
    def __create_new_dialog(self, headers) -> str:
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
            dialog_id = self.__create_new_dialog(self.__headers)

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
                        try:
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
                        except Exception as e:
                            continue
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


def chat_with_kimi_example(content: str = "你好", base_url: str = ''):
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

        return dict_re['result_text']

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

        return dict_re['result_text']['output']

    else:
        logger.error(dict_re['result_text'])


if __name__ == '__main__':

    pass
