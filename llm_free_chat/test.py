from llm_free_chat.llm_chat_free import TencentYB

tc = TencentYB()

headers = {
    'Cookie': '_ga=GA1.2.1761294405.1728537672; _gcl_au=1.1.1132276475.1736386827; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219274dfb768d15-075e76b1b0a2f1-4c657b58-2073600-19274dfb769db%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkyNzRkZmI3NjhkMTUtMDc1ZTc2YjFiMGEyZjEtNGM2NTdiNTgtMjA3MzYwMC0xOTI3NGRmYjc2OWRiIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219274dfb768d15-075e76b1b0a2f1-4c657b58-2073600-19274dfb769db%22%7D; _qimei_uuid42=1921c0e3b2f100c55ea0e03be84de51c2e191d0653; _qimei_fingerprint=c3e64d763595732957eeb61a9b7af521; hy_source=web; _qimei_i_3=5dc82d87955257dec09eab39598771e4a6eca1f2105d0a8bb48f2c592396263d693662943c89e2a181b4; hy_user=134243e8908c4863b52c1aaefb4a2910; hy_token=r65mJjGQM6bnz8CcvJHxZR+uzJ1eCdeAMnc/kYP2aQRr3CbGFH/zV3HyDs+0FFSoE9ah9oeJq1H/rzAq+nldCw==; _qimei_h38=fdedc1ba5ea0e03be84de51c02000007c1930b; _qimei_i_1=78ba6ad4c10f0488c0c5af350ed573b5f7edf6a41a5f57d7b18e7b582493206c616330c63980e1dc8489e3d0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
}


import httpx

payload = {
    "model": "gpt_175B_0404",
    "prompt": f"你好",
    "plugin": "Adaptive",
    "displayPrompt": f"你好",
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

print(httpx.post(url='https://yuanbao.tencent.com/api/chat/a94fd711-e5e9-456d-bd62-b95e3ac1e0d1', headers=headers, json=payload).text)

