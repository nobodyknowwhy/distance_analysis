from datetime import datetime
from base import score_list, standard_list, prompt_list
import os
from tqdm import tqdm

import language_tool_python

# df = pd.read_csv(r'D:\gs\distance_analysis\aes\dataset\ELLIPSE-Corpus\sample_train.csv')

def calculate_grammar_error(text: str) -> int:
    """
    这个是一个检查语法的函数，返回的是这一篇文章有多少语法错误，实际上文章越长，语法错误就有可能越多，但是这并不意味着文章越短评分就应该越高，所以
    可能需要考虑返回一个比例值：（有语法错误的句子）/（总句子）所得到的结果。但是这样实际上也会有些问题，因为如果一个句子出现了多处语法错误，证明
    此文章的水平越低，与只出现一处语法错误的句子不应该一视同仁，经过权衡考虑，打算直接返回章语法错误的数量

    :param text: 输入的文本
    :return: 返回文章语法错误的数量
    """
    tool = language_tool_python.LanguageTool('en-US')  # 对于英语，使用 'en-US'
    try:
        matches = tool.check(text)

        print(matches)
        return len(matches)
    except Exception as e:
        print("Error:", e)
        return 0


base_url = "http://localhost:11434/api"
headers = {
    "Content-Type": "application/json"}


def generate_completion(prompt, model="deepseek-r1", system_prompt=None):
    import requests
    url = f"{base_url}/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False}

    if system_prompt:
        data["prompt"] = f"{system_prompt}\n{prompt}"
    response = requests.post(url, headers=headers, json=data)
    return response.json().get('response', '')


def generate_text(prompt_list:list, score_list:list, standard_list:list, num_generate:int):
    for j in tqdm(range(num_generate), desc='Generating Texts', unit="generation"):
        for prompt_topic in prompt_list:
            for i, score in enumerate(score_list):
                system_prompt = f"You will act as a student with the English levels {score} (range for 1-5), and write a composition according to the corresponding level standards: {standard_list[i]}. Sometimes you can make some mistakes, such as intentional grammar mistakes, intentional misspelling of words, intentional incoherence of sentences, etc., to make you more like a student."
                prompt_big = "the essay you write before still good enough and not match the requirement, you need to change the article you generated above. You can make more mistakes to suit the target requirements just like a student, such as intentional grammar mistakes, intentional spelling mistakes, intentional sentence incoherence and so on."
                prompt_small = "the essay you write before is a little bad and not match the requirement, you need to change the article you generated above. You can make less mistakes to suit the target requirements but don't remove it all."

                prompt = f"""now you are required to generate a text with the essay's topic: '{prompt_topic}'."""

                completion = generate_completion(prompt=prompt, system_prompt=system_prompt)

                file_name = f"D:/gs/distance_analysis/aes/out/{prompt_topic}/{score}/{str(datetime.isoformat(datetime.now())).split('.')[0].replace(':', '-')}.txt"

                os.makedirs(os.path.dirname(file_name), exist_ok=True)

                with open(file_name, "w", encoding="utf-8") as file:
                    file.write(completion)


if __name__ == '__main__':
    generate_text(prompt_list, score_list, standard_list, 200)