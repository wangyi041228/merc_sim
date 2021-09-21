from asyncio import get_event_loop, gather, sleep
import pandas
from aiohttp import ClientSession, TCPConnector
from bs4 import BeautifulSoup
# from bs4.element import NavigableString  # Tag
from json import dumps, loads
from math import floor
import os
# import pandas

U = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
H = {
    'User-Agent': U,
    'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Accept-Charset': 'application/x-www-form-urlencoded; charset=UTF-8',
}


async def get_url(_url):

    while True:
        try:
            async with ClientSession(connector=TCPConnector(ssl=False), headers=H) as session:
                async with session.get(_url) as _r:
                    _t = await _r.text()
            soup = BeautifulSoup(_t, 'html.parser').body
            reveals = soup.find_all('span', {'class': 'card-image'})  # 包括 card-image card-image-doesnt-exist
            _links = ['https://outof.cards' + reveal.find('a')['href'] for reveal in reveals]
            return _links
        except Exception as e:
            print(_url, e)


async def down_url(_url):
    while True:
        try:
            async with ClientSession(connector=TCPConnector(ssl=False), headers=H) as session:
                async with session.get(_url) as _r:
                    _t = await _r.read()
                    _file_name = os.path.join('images', _url.split('/')[-1])
                    while os.path.exists(_file_name):
                        _file_name = _file_name.replace('.', '_.')
                    with open(_file_name, 'wb') as f:
                        f.write(_t)
                    return
        except Exception as e:
            print(_url, e)
            await sleep(1.0)


async def get_pages(_url):
    while True:
        try:
            async with ClientSession(connector=TCPConnector(ssl=False), headers=H) as session:
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
            async with ClientSession(connector=TCPConnector(ssl=False), headers=H) as session:
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
            async with ClientSession(connector=TCPConnector(ssl=False), headers=H) as session:
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
    if not os.path.exists('images'):
        os.makedirs('images')
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


def down_img():
    urls = set()
    for _fname in ('merc.json', 'all.json'):
        with open(_fname, 'r', encoding='utf-8') as f:
            _data = loads(f.read())
            for _item in _data:
                for _img in _item['image_urls']:
                    if _img:
                        urls.add(_img)
    print(len(urls))
    tasks = [down_url(url) for url in urls]
    get_event_loop().run_until_complete(gather(*tasks))


def title_clean(st):
    _t = st
    for _tt in (' 1 Tiers', ' 2 Tiers', ' 3 Tiers', ' 4 Tiers',
                ' IV Tiers', ' III Tiers', ' II Tiers', ' I Tiers', ' Tiers'):
        _t = _t.replace(_tt, '')
    return _t


def merc_data():
    with open('merc_fix.json', 'r', encoding='utf-8') as f:
        _data = loads(f.read())
    merc_out = []
    skill_out = []
    item_out = []
    for _object in _data:
        if _object['titles']:
            _name = _object['name']
            _class = _object['class']
            _titles = _object['titles']
            _titles_a = [title_clean(title) for title in _titles]
            s1 = _titles_a[0]
            s2 = _titles_a[1]
            s3 = _titles_a[2]
            if len(_titles_a) == 6:
                i1 = _titles_a[3]
                i2 = _titles_a[4]
                i3 = _titles_a[5]
            else:
                i1, i2, i3 = None, None, None
            for _skill_name in (s1, s2, s3):
                _skill_name_l = len(_skill_name)
                _skill = {
                    'owner': _name,
                    'name': _skill_name,
                }
                for _ob_ in _object['abilities']:
                    _ob_name = _ob_[0]
                    _ob_level = _ob_name[-1]
                    if len(_ob_name) - _skill_name_l == 2 and _ob_name[:_skill_name_l] == _skill_name:
                        _ob_speed = _ob_[3].replace('Speed ', '') if _ob_[3] else ''
                        _ob_cd = '__' + _ob_[5].replace('Cooldown ', '') if _ob_[5] else ''
                        _skill['a' + _ob_level] = _ob_speed + _ob_cd
                        _skill['e' + _ob_level] = _ob_[1]
                        _skill['school'] = _ob_[6]
                skill_out.append(_skill)

            for _item_name in (i1, i2, i3):
                if not _item_name:
                    continue
                _item_name_l = len(_item_name)
                _item = {
                    'owner': _name,
                    'name': _item_name,
                }
                for _ob_ in _object['items']:
                    _ob_name = _ob_[0]
                    _ob_level = _ob_name[-1]
                    if len(_ob_name) - _item_name_l == 2 and _ob_name[:_item_name_l] == _item_name:
                        _item['e' + _ob_level] = _ob_[1]
                item_out.append(_item)
            _item_o = []
            _merc = {
                'name': _name,
                'class': _class,
                's1': s1,
                's2': s2,
                's3': s3,
                'i1': i1,
                'i2': i2,
                'i3': i3,
            }

            _status = _object['status']
            for _i in range(30):
                _merc['a' + str(_i + 1)] = _status[_i][1] + '__' + _status[_i][2]
            merc_out.append(_merc)
    with open('merc_out.json', 'w', encoding='utf-8') as f:
        print(dumps(merc_out), file=f)
    pandas.read_json('merc_out.json').to_excel('merc_out.xlsx', index=None)
    with open('skill_out.json', 'w', encoding='utf-8') as f:
        print(dumps(skill_out), file=f)
    pandas.read_json('skill_out.json').to_excel('skill_out.xlsx', index=None)
    with open('item_out.json', 'w', encoding='utf-8') as f:
        print(dumps(item_out), file=f)
    pandas.read_json('item_out.json').to_excel('item_out.xlsx', index=None)


if __name__ == '__main__':
    # dump_merc()
    # dump_data()
    # down_img()
    merc_data()

    # 测试
    # t_t = [down_url('https://aaa')]
    # t_r = get_event_loop().run_until_complete(gather(*t_t))
    # print(t_r[0])
