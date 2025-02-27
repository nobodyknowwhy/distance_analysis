import multiprocessing as mp
import os
import random
import re
from io import BytesIO

import httpx
from PIL import Image
from bs4 import BeautifulSoup
from loguru import logger
from tqdm import tqdm


def get_tower_img_mp(index: int, div, list_tower_type):
    div = BeautifulSoup(div, 'html.parser')
    a_tags = div.find_all('a')

    progress_par = tqdm(a_tags, desc=f"正在获取{list_tower_type[index]}牌信息")

    for a in progress_par:
        img_tags = a.find('img')
        img_link = 'https:' + img_tags.get('src')
        tower_name = a.get_text().strip()
        tower_name = re.sub('[0-9]{1,2}', '', tower_name)

        img_obj = BytesIO(httpx.get(img_link).content)

        os.makedirs(os.path.join(os.getcwd(), 'tower_img'), exist_ok=True)

        Image.open(img_obj).resize((77, 140)).save(f"./tower_img/{tower_name}.gif", format='gif')


def get_tower_img_from_url(url: str, mp_run: bool):
    res = httpx.get(url)

    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')

        divs = soup.find_all('div', class_='taluo_jieshi')

        list_tower_type = ['主', '权杖（火）', '圣杯（水）', '宝剑（风）', '星币（土）']

        if not mp_run:

            for index, div in enumerate(divs):
                a_tags = div.find_all('a')

                progress_par = tqdm(a_tags, desc=f"正在获取{list_tower_type[index]}牌信息")

                for a in progress_par:
                    img_tags = a.find('img')
                    img_link = 'https:' + img_tags.get('src')
                    tower_name = a.get_text().strip()
                    tower_name = re.sub('[0-9]{1,2}', '', tower_name)

                    img_obj = BytesIO(httpx.get(img_link).content)

                    os.makedirs(os.path.join(os.getcwd(), 'tower_img'), exist_ok=True)

                    Image.open(img_obj).resize((77, 140)).save(f"./tower_img/{tower_name}.gif", format='gif')

                progress_par.set_description(f"{list_tower_type[index]}牌信息获取完成！")
        else:
            p_list = []
            for index, div in enumerate(divs):
                p = mp.Process(target=get_tower_img_mp, args=(index, str(div), list_tower_type))
                p_list.append(p)
                p.start()
            for p in p_list:
                p.join()

    else:
        logger.error(f"Failed to retrieve the webpage. Status code: {res.status_code}")


def get_meaning_of_tower(url: str):
    res = httpx.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    meaning_all = soup.find('div', class_='show_cnt').find_all('p')

    mark_text = ''
    meaning_list = {}
    for index, meaning in enumerate(meaning_all):
        if '解释' in meaning.text:
            mark_text = '解释'
            meaning_list[mark_text] = ''
            continue
        if '解读' in meaning.text:
            mark_text = '解读'
            meaning_list[mark_text] = ''
            continue
        if '正位' in meaning.text:
            mark_text = '正位'
            meaning_list[mark_text] = ''
            continue
        if '逆位' in meaning.text:
            mark_text = '逆位'
            meaning_list[mark_text] = ''
            continue
        if '大体上的意义' in meaning.text:
            mark_text = '大体'
            meaning_list[mark_text] = ''
            continue
        if '倒立的' in meaning.text:
            mark_text = '倒立'
            meaning_list[mark_text] = ''
            continue
        if '两性关系上的意义' in meaning.text:
            mark_text = '两性'
            meaning_list[mark_text] = ''
            continue
        meaning_list[mark_text] += meaning.text

    return meaning_list


def get_random_tower(num: int, img_dir: str, prob_0: float) -> list:
    tower_names = [f.replace('.gif', '') for f in os.listdir(img_dir)]

    dict_output = []
    for _ in range(num):
        target_idx = random.randint(0, len(tower_names) - 1)
        is_reverse = 0 if random.random() < prob_0 else 1
        dict_output.append((tower_names[target_idx], is_reverse))
    return dict_output


if __name__ == '__main__':
    # get_tower_img_from_url(r"https://www.shenpowang.com/taluopai/jieshi/", mp_run=True)
    # logger.info(get_random_tower(10, "./tower_img", 0.7))
    a = get_meaning_of_tower("https://www.shenpowang.com/taluopai/jieshi/d23107.html")

    for x, y in a.items():
        logger.info(x)
        logger.info(y)
        logger.warning('*******************************')