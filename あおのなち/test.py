from bs4 import BeautifulSoup

with open(r"D:\gs\distance_analysis\あおのなち\ori_html\text.html", "r", encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')


for item in soup.find_all('div', class_='opus-card--with-cover'):
    chapter_url = 'https:' + item.find('a').get('href')
    print(chapter_url)