import json
import multiprocessing as mp
import os.path

from loguru import logger
import httpx
from bs4 import BeautifulSoup


def get_lines_from_prts(operator_name: str, share_list=[])->list:
    res = httpx.get(f"https://prts.wiki/w/{operator_name}/语音记录")

    soup = BeautifulSoup(res.text, 'html.parser')

    lines = soup.find_all('div', class_='voice-item-detail', attrs={'data-kind-name': '中文'})

    dataset_dict = {"instruction": '', "input": '', 'output': ''}

    for line in lines:
        dataset_dict['output'] = line.text
        share_list.append(dataset_dict)

    return share_list

def get_lines_from_prts_mp(operator_name_list:list)->list:
    with mp.Manager() as manager:
        share_list = manager.list([])
        p_list = []
        for operator_name in operator_name_list:
            p = mp.Process(target=get_lines_from_prts, args=(operator_name, share_list))
            p_list.append(p)
            p.start()

        for p in p_list:
            p.join()

        return list(share_list)


def save_jsonlist(lines_list:list, save_path:str):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(lines_list, f, indent=4, ensure_ascii=False)



def adding_instruction_in_json(dataset_json_path, save_path):
    with open(dataset_json_path, 'r', encoding='utf-8') as f:
        dataset_json = json.load(f)

    for item in dataset_json:
        if item['instruction']:
            continue
        logger.warning(f"*********************************************************************************************")
        logger.info(f"instruction_now: {item['instruction']}")
        logger.success(f"output: {item['output']}")
        new_instruction = input()
        if not new_instruction:
            continue

        if new_instruction == 'end':
            break

        item['instruction'] = new_instruction

    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(dataset_json, f, indent=4, ensure_ascii=False)



if __name__ == '__main__':
    # operator_name_list = ['阿米娅', '阿米娅(医疗)', '阿米娅(近卫)']
    # lines_of_operator = get_lines_from_prts_mp(operator_name_list)
    # save_jsonlist(lines_of_operator,
    #               r"D:\gs\distance_analysis\lora_arknight\dataset\amiya.json")

    adding_instruction_in_json(r"D:\gs\distance_analysis\lora_arknight\dataset\amiya.json", r"D:\gs\distance_analysis\lora_arknight\dataset\amiya.json")
