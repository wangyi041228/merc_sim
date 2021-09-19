import json
from bs4 import BeautifulSoup
from bs4.element import NavigableString  # Tag
import pandas
import asyncio
import aiohttp

links = [
    'https://outof.cards/hearthstone/'
    '3623-who-are-the-caster-hearthstone-mercenaries-all-18-collectible-mercenaries',
    'https://outof.cards/hearthstone/'
    '3622-who-are-the-fighter-hearthstone-mercenaries-all-18-collectible-mercenaries',
    'https://outof.cards/hearthstone/'
    '3621-who-are-the-protector-hearthstone-mercenaries-all-16-collectible-launch-mercenaries',
]


async def get_url(_url):
    while True:
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.get(_url) as _r:
                    _t = await _r.text()
            soup = BeautifulSoup(_t, 'html.parser')
            reveals = soup.body.find('p', {'class': 'card-reveals'}).find_all('span', {'class': 'card-image'})
            _links = ['https://outof.cards' + reveal.find('a')['href'] for reveal in reveals]
            return _links
        except Exception as e:
            print(_url, e)


async def work(_url):
    while True:
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.get(_url) as _r:
                    _t = await _r.text()
            soup = BeautifulSoup(_t, 'html.parser')

            section = soup.body.find('section', {'class': 'main has-sidebar active-tab'})
            m_name, m_class = section.find('p').text.replace(' Mercenary.', '').split(' is a ')

            _images = section.find_all('span', {'class': 'card-image'})
            images_urls = [image.find('a').find('img')['src'] for image in _images]

            _titles = section.find_all('h5')
            titles = [title.text for title in _titles]

            _abilities = section.find_all('div', {'class': 'hearth-mercenary-card-rank-embed '
                                                           'hearth-mercenary-ability-rank-embed'})
            abilities = []
            for _ability in _abilities:
                name = _ability.find('div', {'class': 'rank-name'}).text
                text = _ability.find('div', {'class': 'rank-text'}).text
                data = [name, text]
                _level = _ability.find('div', {'class': 'rank-meta-item rank-meta-level'})
                if _level:
                    level = _level.find('span').text
                    data.append(level)
                _speed = _ability.find('div', {'class': 'rank-meta-item rank-meta-speed'})
                if _speed:
                    speed = _speed.find('span').text
                    data.append(speed)
                _cost = _ability.find('div', {'class': 'rank-meta-item rank-meta-cost'})
                if _cost:
                    cost = _cost.find('span').text
                    data.append(cost)
                _cd = _ability.find('div', {'class': 'rank-meta-item rank-meta-cooldown'})
                if _cd:
                    cd = _cd.find('span').text
                    data.append(cd)
                _school = _ability.find('div', {'class': 'rank-meta-item rank-meta-spell-school '
                                                         'rank-meta-spell-school-nature'})
                if _school:
                    school = _school.find('span').text
                    data.append(school)
                abilities.append(data)

            _items = section.find_all('div', {'class': 'hearth-mercenary-card-rank-embed '
                                                       'hearth-mercenary-equipment-rank-embed'})
            items = []
            for _item in _items:
                name = _item.find('div', {'class': 'rank-name'}).text
                text = _item.find('div', {'class': 'rank-text'}).text
                data = [name, text]
                _cost = _item.find('div', {'class': 'rank-meta-item rank-meta-cost'})
                if _cost:
                    cost = _cost.find('span').text
                    data.append(cost)

                items.append(data)

            sta = [[td_node.text for td_node in tr_node.find_all('td')] for tr_node in section.find('tbody').find_all('tr')]

            print(m_name)
            print(m_class)
            print()
            for aa in (images_urls, titles, abilities, items):
                for ab in aa:
                    print(ab)
            print(sta)
            return
        except Exception as e:
            print(_url, e)


if __name__ == '__main__':
    tasks = [get_url(links[i]) for i in range(len(links))]
    urls__ = asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
    urls = urls__[0] + urls__[1] + urls__[2]
    for url in urls:
        print(url)
    tasks = [work(urls[i]) for i in range(len(urls))]
    temp_rs = asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
