import os
import re
import multiprocessing as mp

import pandas as pd

def remove_think_tag(file_path:str, score:int)->list:
    with open(file_path, 'r', encoding='utf-8') as f:
        a = f.read()


    return [re.sub(r'<think>.*?</think>|\*\*.*?\*\*', '', a, flags=re.DOTALL).strip(), score]


def run_remove_tag_mp(root_name:str, file_name_list:list, share_list:list):
    for file_name in file_name_list:

        file_path = os.path.join(root_name, file_name)
        score = os.path.basename(root_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            a = f.read()

        if '---' in a:
            share_list.append([a.split('---')[1].strip(), score])
        else:
            share_list.append([re.sub(r'<think>.*?</think>|\*\*.*?\*\*', '', a, flags=re.DOTALL).strip(), score])


if __name__ == '__main__':
    with mp.Manager() as manager:
        share_list = manager.list([])
        p_list = []
        for root_name, dir_name_list, file_name_list in os.walk(r"D:\gs\distance_analysis\aes\out\second_clean"):
            P = mp.Process(target=run_remove_tag_mp, args=(root_name, file_name_list, share_list))
            p_list.append(P)
            P.start()

        for p in p_list:
            p.join()

        df = pd.DataFrame(list(share_list), columns=["text", "score"])

        print(df)

        df.to_csv(r"D:\gs\distance_analysis\aes\out\second_clean\test\aes_g_c_v_2clean_full.csv", index=False)


