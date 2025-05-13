import asyncio
import hashlib
import re
import time

import httpx
from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL = "https://www.bilibili.com"


def get_pop_list():
    driver = webdriver.Edge()
    driver.implicitly_wait(10)
    driver.delete_all_cookies()
    driver.get(BASE_URL)

    element = driver.find_elements(By.XPATH, '//div[@class="channel-icons"]/a[@class="channel-icons__item"]')[1]
    href = element.get_attribute("href")
    driver.get(href)

    for i in range(1, 10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)

    time.sleep(2)

    ele_pop_list = driver.find_elements(By.XPATH, '//div[@class="flow-loader"]/ul[@class="card-list"]/div')

    out_list = []
    for pop_item in ele_pop_list:
        href_pop_item = pop_item.find_element(By.XPATH, ".//div/a").get_attribute('href')
        title_pop_item = pop_item.find_element(By.XPATH, ".//div/p").text
        out_list.append((title_pop_item, href_pop_item))

    driver.quit()
    return out_list


async def save_as_html(soup, html_path):
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(soup)


def get_redirect_url(text):
    return BASE_URL + re.search('href="(.*?)"', text).group(1)


def get_str_md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


async def get_pop_info(title_url_pairs):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"}
    async with httpx.AsyncClient() as client:
        tasks_responses = [client.get(url=url, headers=headers) for _, url in title_url_pairs]
        responses = await asyncio.gather(*tasks_responses)

        tasks_soups = [client.get(url=get_redirect_url(response.text), headers=headers) for (title, _), response in
                       zip(title_url_pairs, responses)]
        soups = await asyncio.gather(*tasks_soups)

        tasks_save = [save_as_html(soup.text, f'./result/{get_str_md5(title)}.html') for (title, _), soup in
                      zip(title_url_pairs, soups)]
        await asyncio.gather(*tasks_save)


def main_run():
    title_url_pairs = get_pop_list()
    asyncio.run(get_pop_info(title_url_pairs))


if __name__ == "__main__":
    main_run()
