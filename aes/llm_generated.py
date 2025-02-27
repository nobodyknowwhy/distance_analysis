import requests

base_url = "http://localhost:11434/api"
headers = {
    "Content-Type": "application/json"
}

context = []

def generate_completion(prompt, model="deepseek-r1"):
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