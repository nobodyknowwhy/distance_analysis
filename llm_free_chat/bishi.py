import chardet
from loguru import logger

from llm_free_chat.llm_chat_free import chat_with_kimi_example

prompt = """你现在要总结出以下文本的内容内容，提取其关键信息，分三个段落进行提炼总结，字数总和1000字左右。你的任务只是对给定文章内容进行总结就行，无需进行不必要的补充和对作品的介绍，文章内容如下：\n\n"""
split_interval = 10000

file_path = r"D:\gs\distance_analysis\lora_arknight\out\merged.txt"
def detect_encoding(file_path):
    """检测文件的编码"""
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

encoding_method = detect_encoding(file_path)

with open(file_path, 'r', encoding='utf-8') as f:
    content_all = f.read()

    cursor = 0

    len_f = len(content_all)
    mark_end = False
    while cursor < len_f:

        if cursor + split_interval > len_f:
            content_now = content_all[cursor:]
            mark_end = True
        else:
            left_point = cursor
            cursor += split_interval
            while cursor < len_f and content_all[cursor] != '\n':
                cursor += 1

            content_now = content_all[left_point:cursor]

        logger.info(content_now)
        if mark_end:
            break

        re = chat_with_kimi_example(rf"{prompt} {content_now}")

        break


