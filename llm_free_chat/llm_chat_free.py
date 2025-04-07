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
                                if part_text == '获取流式HTTP请求输出':
                                    continue
                                if is_print:
                                    print(part_text, end='')
                                output_str += part_text
                    print()
                else:
                    raise ValueError(f"请求失败啦！状态码: {response.status_code}，呜呜呜~")

        base_url = f'https://kimi.moonshot.cn/chat/{dialog_id}'

        return {'base_url': base_url, 'result_text': output_str, 'success': True}


if __name__ == '__main__':
    kimi = KIMI()

    logger.info(f"类介绍:{kimi}")

    logger.info(f"类详细介绍:{kimi.__repr__()}")

    dict_re = kimi.chat(content="哈哈害，我又来了啊！", create_new_dialog=True)

    if dict_re['success']:

        logger.warning(f"对话链接：\n{dict_re['base_url']}")

        logger.success(f"对话结果：\n{dict_re['result_text']}")

    else:
        logger.error(dict_re['result_text'])
