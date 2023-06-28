from bs4 import BeautifulSoup
from requests import get
from fake_useragent import UserAgent
from random import choice, randint as r

def list_type():
    resp = get('https://anekdotbar.ru', headers={'User-Agent': UserAgent().random})
    soup = BeautifulSoup(resp.content, 'html.parser')
    items = soup.find('div', class_='menu')
    a = items.find_all('li')
    b = [i.a.get_attribute_list('href')[0] for i in a]
    return choice(b)

def anekdot(typ):
    resp = get(f'https://anekdotbar.ru{typ}page/{r(1, 5)}/', headers={'User-Agent': UserAgent().random})
    soup = BeautifulSoup(resp.content, 'html.parser')
    item = soup.find_all('div', class_='tecst')
    items = [i.get_text(strip=True).replace('-', '\n-') for i in item]
    items_all = [i[:i.rfind('+')] for i in items]
    return choice(items_all)

if __name__ == '__main__':
    print(anekdot(list_type()))
