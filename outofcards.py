from asyncio import get_event_loop, gather, sleep
import pandas
from aiohttp import ClientSession, TCPConnector
from bs4 import BeautifulSoup
# from bs4.element import NavigableString  # Tag
from json import dumps
from math import floor
# import pandas


async def get_url(_url):
    while True:
        try:
            async with ClientSession(connector=TCPConnector(ssl=False)) as session:
                async with session.get(_url) as _r:
                    _t = await _r.text()
            soup = BeautifulSoup(_t, 'html.parser').body
            reveals = soup.find_all('span', {'class': 'card-image'})  # 包括 card-image card-image-doesnt-exist
            _links = ['https://outof.cards' + reveal.find('a')['href'] for reveal in reveals]
            return _links
        except Exception as e:
            print(_url, e)


async def get_pages(_url):
    while True:
        try:
            async with ClientSession(connector=TCPConnector(ssl=False)) as session:
                async with session.get(_url) as _r:
                    _t = await _r.text()
            soup = BeautifulSoup(_t, 'html.parser').body
            pages = int(soup.find('ul', {'class': 'pagination'}).find_all('li')[-2].find('a').text)
            return pages
        except Exception as e:
            print(_url, e)


async def work(_url):
    while True:
        try:
            async with ClientSession(connector=TCPConnector(ssl=False)) as session:
                async with session.get(_url) as _r:
                    _t = await _r.text()
            soup = BeautifulSoup(_t, 'html.parser')
            section = soup.body.find('section', {'class': 'main has-sidebar active-tab'})

            m_name, m_class = section.find('p').text.replace(' Mercenary.', '').split(' is a ')

            _images = section.find_all('span', {'class': 'card-image'})
            images_urls = [image.find('img')['src'] if image.find('img') else None for image in _images]

            _titles = section.find_all('h5')
            titles = [title.text for title in _titles]

            _abilities = section.find_all('div', {'class': 'hearth-mercenary-ability-rank-embed'})
            abilities = []
            for _ability in _abilities:
                name = _ability.find('div', {'class': 'rank-name'}).text
                text = _ability.find('div', {'class': 'rank-text'}).text
                _level = _ability.find('div', {'class': 'rank-meta-level'})
                level = _level.find('span').text if _level else None
                _speed = _ability.find('div', {'class': 'rank-meta-speed'})
                speed = _speed.find('span').text if _speed else None
                _cost = _ability.find('div', {'class': 'rank-meta-cost'})
                cost = _cost.find('span').text if _cost else None
                _cd = _ability.find('div', {'class': 'rank-meta-cooldown'})
                cd = _cd.find('span').text if _cd else None
                _school = _ability.find('div', {'class': 'rank-meta-spell-school'})
                school = _school.find('span').text if _school else None
                abilities.append([name, text, level, speed, cost, cd, school])

            _items = section.find_all('div', {'class': 'hearth-mercenary-equipment-rank-embed'})
            items = []
            for _item in _items:
                name = _item.find('div', {'class': 'rank-name'}).text
                text = _item.find('div', {'class': 'rank-text'}).text
                _cost = _item.find('div', {'class': 'rank-meta-cost'})
                cost = _cost.find('span').text if _cost else None

                items.append([name, text, cost])

            sta = [[td_node.text for td_node in tr_node.find_all('td')] for tr_node in
                   section.find('tbody').find_all('tr')]

            # # 验算
            # atk = [int(lv[1]) for lv in sta]
            # hp = [int(lv[2]) for lv in sta]
            #
            # _all_wrong = False
            # if len(atk) != 30 or len(hp) != 30:
            #     _all_wrong = True
            # if _all_wrong:
            #     for line in sta:
            #         print(line)
            # else:
            #     d_atk = (atk[-1] - atk[0]) / 29
            #     d_hp = (hp[-1] - hp[0]) / 29
            #     for i in range(1, 29):
            #         _line_wrong = False
            #         atk_cal = atk[0] + int(floor(d_atk * i))
            #         if atk[i] != atk_cal:
            #             _line_wrong = True
            #         hp_cal = hp[0] + int(floor(d_hp * i))
            #         if hp[i] != hp_cal:
            #             _line_wrong = True
            #         if _line_wrong:
            #             print(sta[i], '计算值', [i + 1, atk_cal, hp_cal])
            _return_ = {
                'url': _url,
                'name': m_name,
                'class': m_class,
                'image_urls': images_urls,
                'titles': titles,
                'abilities': abilities,
                'items': items,
                'status': sta,
            }
            return _return_
        except Exception as e:
            print(_url, e)
            await sleep(1.0)


async def work2(_url):
    while True:
        try:
            async with ClientSession(connector=TCPConnector(ssl=False)) as session:
                async with session.get(_url) as _r:
                    _t = await _r.text()
            soup = BeautifulSoup(_t, 'html.parser').body
            c_name = soup.find('section', {'class': 'main content-before'}).find('h1').text
            main = soup.find('section', {'main has-sidebar active-tab'})
            _images = main.find_all('span', {'class': 'card-image'})
            images_urls = [image.find('img')['src'] if image.find('img') else None for image in _images]
            _li = main.find('ul', {'class': 'item-stats card-stats'}).find_all('li')[3:]
            li = [line.find_all('span')[-1].text for line in _li]
            _text = main.find('p')
            text = _text.text if _text else None

            _return_ = {
                'url': _url,
                'name': c_name,
                'image_urls': images_urls,
                'status': li,
                'text': text,
            }
            return _return_
        except Exception as e:
            print(_url, e)
            await sleep(1.0)


def dump_merc():
    links = [
        'https://outof.cards/hearthstone/mercenaries/heroes/?page=1',
        'https://outof.cards/hearthstone/mercenaries/heroes/?page=2',
        'https://outof.cards/hearthstone/mercenaries/heroes/?page=3',
        'https://outof.cards/hearthstone/mercenaries/heroes/?page=4',
        'https://outof.cards/hearthstone/mercenaries/heroes/?page=5',
    ]
    tasks = [get_url(links[i]) for i in range(len(links))]
    _urls_ = get_event_loop().run_until_complete(gather(*tasks))
    urls = []
    for i in range(len(_urls_)):
        urls += _urls_[i]
    tasks = [work(urls[i]) for i in range(len(urls))]
    temp_rs = get_event_loop().run_until_complete(gather(*tasks))
    with open('merc.json', 'w', encoding='utf-8') as f:
        print(dumps(temp_rs), file=f)
    pandas.read_json('merc.json').to_excel('merc.xlsx', index=None)


def dump_data():
    tasks = [get_pages('https://outof.cards/hearthstone/cards/?page=1&card_set=66')]
    _pages_ = get_event_loop().run_until_complete(gather(*tasks))
    links = [f'https://outof.cards/hearthstone/cards/?page={i}&card_set=66' for i in range(1, _pages_[0] + 1)]
    tasks = [get_url(links[i]) for i in range(len(links))]
    _urls_ = get_event_loop().run_until_complete(gather(*tasks))
    urls = []
    for i in range(len(_urls_)):
        urls += _urls_[i]
    tasks = [work2(urls[i]) for i in range(len(urls))]
    temp_rs = get_event_loop().run_until_complete(gather(*tasks))
    with open('all.json', 'w', encoding='utf-8') as f:
        print(dumps(temp_rs), file=f)
    pandas.read_json('all.json').to_excel('all.xlsx', index=None)


if __name__ == '__main__':
    dump_merc()
    dump_data()

    # 测试
    # t_t = [work2('https://outof.cards/hearthstone/cards/15880-claws-of-terror-4')]
    # t_r = get_event_loop().run_until_complete(gather(*t_t))
    # print(t_r[0])
