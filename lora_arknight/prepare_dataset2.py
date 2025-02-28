import json
import os
import multiprocessing as mp
import re


def get_dataset_mp(file_path:str, dataset_all_list:list, type_format:str='alpaca'):
    last_npc = ''
    dataset_dict = {'instruction': '', 'last_role': '', 'input': '', 'output': ''}
    if type_format == 'alpaca':
        try:
            with open(file_path, 'r', encoding='gbk') as f:
                for line in f:
                    if not (line.startswith('"') or line.startswith('选择')):
                        continue

                    if line.startswith('"阿米娅"'):
                        operator_line = line.split(':')[1].strip()

                        if dataset_dict['last_role'] == "阿米娅":
                            dataset_dict['output'] += operator_line
                        else:
                            dataset_dict['output'] = operator_line

                        dataset_dict['last_role'] = '阿米娅'
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
                            dataset_dict = {'instruction': f'{npc_line}', 'last_role': f'{npc_name}', 'input': '',
                                            'output': ''}

                        last_npc = npc_name
        except Exception as e:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if not (line.startswith('"') or line.startswith('选择')):
                        continue

                    if line.startswith('"阿米娅"'):
                        operator_line = line.split(':')[1].strip()

                        if dataset_dict['last_role'] == "阿米娅":
                            dataset_dict['output'] += operator_line
                        else:
                            dataset_dict['output'] = operator_line

                        dataset_dict['last_role'] = '阿米娅'
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
                                dataset_dict = {'instruction': f'{npc_line}', 'last_role': f'{npc_name}',
                                                'input': '',
                                                'output': ''}
                        else:
                            dataset_dict = {'instruction': f'{npc_line}', 'last_role': f'{npc_name}', 'input': '',
                                            'output': ''}

                        last_npc = npc_name



def create_history_from_json(json_role_path:str):
    with open(json_role_path, 'r', encoding='utf-8') as f:
        role_data = json.load(f)

    out_put_dataset_list = []

    out_put_dataset = {'instruction':'', 'input':'', 'output': '', 'system': '', 'history':[]}

    last_role = ''
    for conversations in role_data:
        if conversations['user_role'] == last_role:
            out_put_dataset['history'].append([conversations['instruction'], conversations['output']])
        else:
            try:
                list_final = out_put_dataset['history'].pop(-1)
                out_put_dataset['instruction'] = list_final[0]
                out_put_dataset['output'] = list_final[1]
                out_put_dataset['system'] = f'你现在是阿米娅，用户现在是{last_role}'
                out_put_dataset_list.append(out_put_dataset)
            except Exception as e:
                no_use = 0
            finally:
                out_put_dataset = {'instruction': '', 'input': '', 'output': '', 'system': '', 'history': []}
                out_put_dataset['history'].append([conversations['instruction'], conversations['output']])
                last_role = conversations['user_role']

    return out_put_dataset_list


def get_special_npc(npc_name:str, json_path, out_path):
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


def main_run(run_mp:bool=True):
    if run_mp:
        p_list = []
        with mp.Manager() as manager:
            dataset_all_list = manager.list([])
            for root_name, dir_list, file_list in os.walk(r"D:/me/主线"):
                for file_name in file_list:
                    file_path = os.path.join(root_name, file_name)

                    p = mp.Process(target=get_dataset_mp, args=(file_path, dataset_all_list))
                    p_list.append(p)
                    p.start()

            for p in p_list:
                p.join()

            return list(dataset_all_list)
    else:
        dataset_all_list = []
        for root_name, dir_list, file_list in os.walk(r"D:/me/主线"):
            for file_name in file_list:
                file_path = os.path.join(root_name, file_name)
                get_dataset_mp(file_path, dataset_all_list)

        return dataset_all_list


if __name__ == '__main__':

    dataset_all_list = main_run(False)

    with open(r"D:/gs/distance_analysis/lora_arknight/dataset/amiya_all_role_noshulff9-34.json", 'w', encoding='utf-8') as f:
        json.dump(dataset_all_list, f, indent=4, ensure_ascii=False)

    # get_quality_lines(r"D:/gs/distance_analysis/lora_arknight/dataset/amiya_all.json", r"D:/gs/distance_analysis/lora_arknight/dataset/amiya_arknight.json")

    # get_special_npc('特蕾西娅', r"D:/gs/distance_analysis/lora_arknight/dataset/amiya2.json", r"D:/gs/distance_analysis/lora_arknight/dataset/amiya_theresa.json")

    # dataset_all_list = create_history_from_json(r"D:/gs/distance_analysis/lora_arknight/dataset/amiya_all_role_noshulff9-34.json")
    #
    # with open(r"D:/gs/distance_analysis/lora_arknight/dataset/amiya_all_role_noshulff9-34_history.json", 'w', encoding='utf-8') as f:
    #     json.dump(dataset_all_list, f, indent=4, ensure_ascii=False)




