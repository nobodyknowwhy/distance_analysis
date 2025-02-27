import httpx

from bs4 import BeautifulSoup

res = httpx.get(r"https://ollama.com/search").text

print(res)