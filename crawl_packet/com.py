import httpx
from bs4 import BeautifulSoup

header = {'User-Agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"""}

html_text = httpx.get(r"https://www.bilibili.com/anime/", headers=header).text

soup = BeautifulSoup(html_text, 'html.parser')


print(soup)