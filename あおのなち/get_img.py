import os.path
import multiprocessing as mp
import time

import httpx
from tqdm import tqdm
from bs4 import BeautifulSoup


def save_img_from_url(save_path:str, url:str=r"https://www.bilibili.com/opus/994524347695628290"):
    header = {
        'User-Agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"""
    }

    res = httpx.get(url, headers=header)

    soup = BeautifulSoup(res.text, "html.parser")


    title, chapter = soup.find('title').text.split('-')[0].strip().split()

    target_save_path = os.path.join(save_path, title, chapter)

    os.makedirs(target_save_path, exist_ok=True)

    for index, item in enumerate(soup.find_all('div', class_='b-img sleepy'), start=1):
        img_item = item.find('img')
        img_url = 'https:' + img_item.get('src')
        res = httpx.get(img_url)

        target_save_img = os.path.join(target_save_path, f'{index}.jpg')

        with open(target_save_img, 'wb') as f:
            f.write(res.content)

if __name__ == '__main__':
    p_list = []
    save_path = r"D:\gs\distance_analysis\あおのなち"

    with open(r"D:\gs\distance_analysis\あおのなち\ori_html\text.html", "r", encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    for item in tqdm(soup.find_all('div', class_='opus-card'), desc="processing data"):
        chapter_url = 'https:' + item.find('a').get('href')
        chapter_name = item.find('img').get('alt')

        if chapter_name.startswith('与你'):
            try:
                save_img_from_url(save_path=save_path, url=chapter_url)
            except Exception as e:
                import traceback
                from loguru import logger
                logger.error(traceback.format_exception(e))
            time.sleep(60)