import json
import multiprocessing as mp
import os
import re

from loguru import logger


def get_dataset_mp(file_path: str, dataset_all_list: list, main_role_name: str, type_format: str = 'alpaca'):
    last_npc = ''
    dataset_dict = {'instruction': '', 'last_role': '', 'input': '', 'output': ''}

    try:
        with open(file_path, 'r', encoding='gbk') as f:
            a = f.readline()
            encoding_method = 'gbk'
    except Exception as e_error:
        encoding_method = 'utf-8'

    if type_format == 'alpaca':
        try:
            with open(file_path, 'r', encoding=encoding_method) as f:
                for line in f:
                    if not (line.startswith('"') or line.startswith('选择')):
                        line = line.strip()
                        if line and line != '(特效)':
                            if dataset_dict['last_role'] == main_role_name:
                                dataset_dict['output'] += f'({line})'
                            else:
                                dataset_dict['instruction'] += f'({line})'
                        continue

                    if line.startswith(f'"{main_role_name}"'):
                        operator_line = line.split(':')[1].strip()

                        if dataset_dict['last_role'] == main_role_name:
                            dataset_dict['output'] += operator_line
                        else:
                            dataset_dict['output'] = operator_line

                        dataset_dict['last_role'] = main_role_name
                    else:
                        if line.startswith('选择'):
                            npc_name = '博士'

                            npc_line = re.sub('.*?\"(.*?)\(.*?\)\"', r'\1', line)

                            npc_list = [npc_name, npc_line]

                        else:
                            npc_list = line.split(':')

                            npc_name = npc_list[0].strip().replace('"', '')

                            npc_line = npc_list[1].strip()

                        if dataset_dict['output']:
                            if npc_name == dataset_dict['last_role']:
                                dataset_dict['instruction'] += npc_line
                            else:
                                if dataset_dict['instruction']:
                                    dataset_dict.pop("last_role")
                                    dataset_dict['user_role'] = last_npc
                                    dataset_dict['source_file'] = file_path
                                    dataset_all_list.append(dataset_dict)
                                dataset_dict = {'instruction': f'{npc_line}', 'last_role': f'{npc_name}', 'input': '',
                                                'output': ''}
                        else:
                            if npc_name == dataset_dict['last_role']:
                                dataset_dict['instruction'] += npc_line
                            else:
                                dataset_dict['instruction'] = npc_line
                            dataset_dict = {'instruction': f"{dataset_dict['instruction']}", 'last_role': f'{npc_name}',
                                            'input': '',
                                            'output': ''}

                        last_npc = npc_name
        except Exception as e:
            logger.error(e)


def clean_empty_data(json_path: str, out_path: str, exclusions_list=['input']):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)  # 加载 JSON 数据

    filtered_data = []

    for item in data:
        mark_empty = False
        for key in item:
            if key in exclusions_list:
                continue
            if not item.get(key):
                mark_empty = True
                break

        if not mark_empty:
            filtered_data.append(item)

    with open(out_path, 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, ensure_ascii=False, indent=4)


def create_history_from_json(role_name: str, json_role_path: str):
    with open(json_role_path, 'r', encoding='utf-8') as f:
        role_data = json.load(f)

    out_put_dataset_list = []

    out_put_dataset = {'instruction': '', 'input': '', 'output': '', 'system': '', 'history': []}

    last_role = ''
    for conversations in role_data:
        if conversations['user_role'] == last_role:
            out_put_dataset['history'].append([conversations['instruction'], conversations['output']])
        else:
            try:
                list_final = out_put_dataset['history'].pop(-1)
                out_put_dataset['instruction'] = list_final[0]
                out_put_dataset['output'] = list_final[1]
                out_put_dataset['system'] = f'你现在是{role_name}，用户现在是{last_role}'
                out_put_dataset_list.append(out_put_dataset)
            except Exception as e:
                no_use = 0
            finally:
                out_put_dataset = {'instruction': '', 'input': '', 'output': '', 'system': '', 'history': []}
                out_put_dataset['history'].append([conversations['instruction'], conversations['output']])
                last_role = conversations['user_role']

    return out_put_dataset_list


def get_special_npc(npc_name: str, json_path, out_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)  # 加载 JSON 数据

    filtered_data = [item for item in data if item.get('user_role') == npc_name]

    with open(out_path, 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, ensure_ascii=False, indent=4)


def get_quality_lines(json_path, out_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)  # 加载 JSON 数据

    filtered_data = [item for item in data if len(re.sub('[：，。！\.——？]*?', r'', item.get('output'))) > 8]

    with open(out_path, 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, ensure_ascii=False, indent=4)


def delete_json_item(json_in_path: str, json_out_path: str, pop_list: list, replace_pop: int | str = -1):
    with open(json_in_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)  # 加载 JSON 数据

    for item in json_data:
        for x in pop_list:
            item.pop(x, None)

    if replace_pop != -1:
        for item in json_data:
            for x in pop_list:
                item[x] = replace_pop

    with open(json_out_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)


def main_run(role_name: str, run_mp: bool = True, dir_name: str = r"D:/me/主线"):
    if run_mp:
        p_list = []
        with mp.Manager() as manager:
            dataset_all_list = manager.list([])
            for root_name, dir_list, file_list in os.walk(dir_name):
                for file_name in file_list:
                    file_path = os.path.join(root_name, file_name)

                    p = mp.Process(target=get_dataset_mp, args=(file_path, dataset_all_list, role_name))
                    p_list.append(p)
                    p.start()

            for p in p_list:
                p.join()

            return list(dataset_all_list)
    else:
        dataset_all_list = []
        for root_name, dir_list, file_list in os.walk(dir_name):
            for file_name in file_list:
                file_path = os.path.join(root_name, file_name)
                get_dataset_mp(file_path, dataset_all_list, role_name)

        return dataset_all_list


def create_dataset_json(role_name: str, english_name: str, dir_name: str, run_mp: bool):
    dataset_all_list = main_run(role_name, run_mp, dir_name)

    path_to_data = os.path.join(os.getcwd(), 'dataset', english_name)

    os.makedirs(path_to_data, exist_ok=True)

    json_no_shulff = os.path.join(path_to_data, f'{english_name}_no_shul.json')

    json_one_sigle = os.path.join(path_to_data, f'{english_name}_sig.json')

    json_with_history = os.path.join(path_to_data, f'{english_name}_his.json')

    with open(json_no_shulff, 'w', encoding='utf-8') as f:
        json.dump(dataset_all_list, f, indent=4, ensure_ascii=False)

    delete_json_item(json_no_shulff, json_one_sigle, ['source_file', 'user_role'])

    # get_quality_lines(r"D:/gs/distance_analysis/lora_arknight/dataset/amiya_all.json", r"D:/gs/distance_analysis/lora_arknight/dataset/amiya_arknight.json")

    # get_special_npc('特蕾西娅', r"D:/gs/distance_analysis/lora_arknight/dataset/amiya2.json", r"D:/gs/distance_analysis/lora_arknight/dataset/amiya_theresa.json")

    dataset_all_list = create_history_from_json(role_name, json_no_shulff)

    with open(json_with_history, 'w', encoding='utf-8') as f:
        json.dump(dataset_all_list, f, indent=4, ensure_ascii=False)

    delete_json_item(json_with_history, json_with_history, ['system'], replace_pop=f"请你现在扮演{role_name}，英文名也叫做{english_name}。")

    # clean_empty_data(r"D:/gs/distance_analysis/lora_arknight/dataset/theresa_all_role_noshulff_history.json",
    #                  r"D:/gs/distance_analysis/lora_arknight/dataset/theresa_all_role_noshulff_history_noempty.json",
    #                  ['input'])


if __name__ == '__main__':
    role_name = "普瑞赛斯"

    english_name = "Priestess"

    dir_name = r"D:\me\arknight"

    create_dataset_json(role_name=role_name, english_name=english_name, dir_name=dir_name, run_mp=False)
