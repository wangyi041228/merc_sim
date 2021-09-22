import os
from enum import Enum
from json import loads
from random import randint
from tkinter import *
from tkinter.ttk import *

from PIL import Image, ImageTk, ImageDraw, ImageFont  # ImageGrab, ImageChops

# import ctypes
#
# g_s = ctypes.windll.user32.GetSystemMetrics
# screensize = g_s(78), g_s(79)
font_type = os.sep.join(('font', 'GLEI00M_t.ttf'))
font = ImageFont.truetype(font_type, size=40, index=0, encoding='unic')
with open('data_merc.json', 'r', encoding='utf-8') as _f_:
    d_merc = loads(_f_.read())
with open('data_skill.json', 'r', encoding='utf-8') as _f_:
    d_skill = loads(_f_.read())
with open('data_item.json', 'r', encoding='utf-8') as _f_:
    d_item = loads(_f_.read())
MERC = Enum('MERC', tuple(d_merc[0]))
MERC_L = {}
for _count in range(len(d_merc[0])):
    MERC_L[MERC[d_merc[0][_count]]] = d_merc[1][_count]
MERC_L_R = dict(zip(MERC_L.values(), MERC_L.keys()))
MERC_L_CB = d_merc[1]

RACE = Enum('RACE',
            ('-', 'Tauren', 'Human', 'Orc', 'Beast', 'Demon', 'Murloc', 'Element', 'Night Elf', 'Gnome', 'Undead',
             'Dwarf', 'Blood Elf', 'Troll', 'Half-Orc', 'Dragon', 'Draenei'))
RACE_L = {
    RACE['-']: '无种族',
    RACE['Tauren']: '牛头人',
    RACE['Human']: '人类',
    RACE['Orc']: '兽人',
    RACE['Beast']: '野兽',
    RACE['Demon']: '恶魔',
    RACE['Murloc']: '鱼人',
    RACE['Element']: '元素',
    RACE['Night Elf']: '暗夜精灵',
    RACE['Gnome']: '侏儒',
    RACE['Undead']: '亡灵',
    RACE['Dwarf']: '矮人',
    RACE['Blood Elf']: '血精灵',
    RACE['Troll']: '巨魔',
    RACE['Half-Orc']: '半兽人',
    RACE['Dragon']: '龙',
    RACE['Draenei']: '德莱尼',
}
M_TYPE = Enum('M_TYPE', ('-', 'Protector', 'Fighter', 'Caster'))
M_TYPE_L = {
    M_TYPE['-']: '中立',
    M_TYPE['Protector']: '护卫',
    M_TYPE['Fighter']: '斗士',
    M_TYPE['Caster']: '施法者',
}
S_TYPE = Enum('S_TYPE', ('-', 'Arcane', 'Fire', 'Fel', 'Frost', 'Holy', 'Nature', 'Shadow'))
S_TYPE_L = {
    S_TYPE['-']: '无',
    S_TYPE['Arcane']: '奥术',
    S_TYPE['Fire']: '火焰',
    S_TYPE['Fel']: '邪能',
    S_TYPE['Frost']: '冰霜',
    S_TYPE['Holy']: '神圣',
    S_TYPE['Nature']: '自然',
    S_TYPE['Shadow']: '暗影',
}

SKILL = Enum('SKILL', tuple(d_skill[0]))
SKILL_L = {}
SKILL_D = {}
SKILL_L_CB_F = {}
for _count in range(len(d_skill[0])):
    SKILL_L[SKILL[d_skill[0][_count]]] = d_skill[1][_count]
    s_cd = []
    for _ii in range(1, 6):
        _t_ = d_skill[2 + _ii][_count]
        if _t_ is str and '__' in _t_:
            s_c = _t_.split('__')
            _s_, _cd_ = int(s_c[0]), int(s_c[1])
        else:
            _s_, _cd_ = _t_, 0
        s_cd.append((_s_, d_skill[7 + _ii][_count], _cd_))
    SKILL_D[SKILL[d_skill[0][_count]]] = [S_TYPE[d_skill[2][_count]]] + s_cd
SKILL_L_R = dict(zip(SKILL_L.values(), SKILL_L.keys()))
SKILL_L_CB = d_skill[1]
SKILL_LEVEL_CB = (1, 2, 3, 4, 5)
SKILL_TARGET_CB = (0, 1, 2, 3, 4, 5, 6, 7, -1, -2, -3, -4, -5, -6, -7)

ITEM = Enum('ITEM', tuple(d_item[0]))
ITEM_L = {}
ITEM_D = {}
for _count in range(len(d_item[0])):
    ITEM_L[ITEM[d_item[0][_count]]] = d_item[1][_count]
    m_l = 2
    while not d_item[m_l][_count]:
        m_l += 1
    ITEM_D[ITEM[d_item[0][_count]]] = [m_l - 1, d_item[2][_count], d_item[3][_count], d_item[4][_count], d_item[5][_count]]
ITEM_L_R = dict(zip(ITEM_L.values(), ITEM_L.keys()))
ITEM_L_CB = d_item[1]
ITEM_L_CB_F = {}
ITEM_LEVEL_CB = (1, 2, 3, 4)

D = {}
for _count in range(len(d_merc[0])):
    # 12到41是攻防
    a_h = [(1, 1)]
    for _cc in range(12, 42):
        _a_ = d_merc[_cc][_count].split('__')
        a_h.append((int(_a_[0]), int(_a_[1])))
    D[MERC[d_merc[0][_count]]] = [M_TYPE[d_merc[2][_count]], RACE[d_merc[3][_count]],
                                  (ITEM[d_merc[4][_count]], ITEM[d_merc[5][_count]],
                                   ITEM[d_merc[6][_count]], ITEM[d_merc[7][_count]]),
                                  (SKILL[d_merc[8][_count]], SKILL[d_merc[9][_count]],
                                   SKILL[d_merc[10][_count]], SKILL[d_merc[11][_count]]), a_h]
    SKILL_L_CB_F[MERC[d_merc[0][_count]]] = [SKILL_L[SKILL['-']], SKILL_L[SKILL[d_merc[8][_count]]], SKILL_L[SKILL[d_merc[9][_count]]],
                                             SKILL_L[SKILL[d_merc[10][_count]]], SKILL_L[SKILL[d_merc[11][_count]]]]
    ITEM_L_CB_F[MERC[d_merc[0][_count]]] = [ITEM_L[ITEM['-']], ITEM_L[ITEM[d_merc[4][_count]]], ITEM_L[ITEM[d_merc[5][_count]]],
                                            ITEM_L[ITEM[d_merc[6][_count]]], ITEM_L[ITEM[d_merc[7][_count]]]]
L = 30  # 初始等级
M_SET = [(MERC[n], L, D[MERC[n]][4][L][0], D[MERC[n]][4][L][1], 0, 0, (ITEM['-'], 1), (SKILL['-'], 1, 0), ()) for n in (
    '-', 'Cariel Roame', 'Tyrande', 'Xyrella')]
params = {
    'w': 1520,
    'h': 850,
    'x': 50,
    'y': 50,
    't': 1,
    'e': [M_SET[0], M_SET[0], M_SET[1], M_SET[2], M_SET[3], M_SET[0], M_SET[0]],
    'a': [M_SET[0], M_SET[0], M_SET[1], M_SET[2], M_SET[3], M_SET[0], M_SET[0]]
}


def get_info(_f):
    return [[f[i].get() for i in range(11)] for f in _f]


class MainWindow(Tk):
    class SideWindow(Toplevel):
        def __init__(self):
            super().__init__()
            self.parent = self.nametowidget(self.winfo_parent())
            self.t = params['t']
            self.title(f'第{str(self.t)}回合')
            self.w = params['w']
            self.h = params['h']
            self.cx = 0
            self.cy = 0
            self.x = params['x']
            self.y = params['y']
            self.merc_img = {
                'e': [None] * 7,
                'a': [None] * 7
            }
            self.geometry(f'{str(self.w)}x{str(self.h)}+{str(self.x)}+{str(self.y)}')
            self.resizable(False, False)

            self.bg = Label(self, image=self.parent.bgimg)
            self.bg.pack(fill=BOTH)
            self.bg.place(x=-2, y=-2)

            self.canvas = Canvas(self, width=1385, height=550, bd=-2)
            self.canvas_img = Image.new('RGBA', (1385, 550))
            self.canvas_paint = Image.new('RGBA', (1385, 550))
            with Image.open('canvas.png') as im:
                self.canvas_img.paste(im.convert('RGBA'), (0, 0))
            self.canvas_imgp = None
            self.canvas.pack()
            self.canvas.place(x=60, y=150)
            self.canvas.bind('<Button-1>', self.canvas_press)
            self.canvas.bind('<ButtonRelease-1>', self.canvas_release)

            self.widgets_1 = []
            self.widgets_swap_1 = []
            self.widgets_update_1 = []
            self.widgets_2 = []
            self.widgets_swap_2 = []
            self.widgets_update_2 = []

            for _c, _w, _s, _u, _y in (
                    ('e', self.widgets_1, self.widgets_swap_1, self.widgets_update_1, 0),
                    ('a', self.widgets_2, self.widgets_swap_2, self.widgets_update_2, 750)):
                _i = 0
                for merc in params[_c]:
                    _x = _i * 205 + 50
                    _merc_name = merc[0]
                    _level = merc[1]
                    _item = merc[6]
                    if not _item:
                        _item = (ITEM['-'], 1)
                    elif _item[1] < ITEM_D[_item[0]][0]:
                        _item = (_item[0], ITEM_D[_item[0]][0])
                    _skill = merc[7]
                    if not _skill:
                        _skill = (SKILL['-'], 1, 0)
                    _passive = merc[8]

                    _merc_combobox = Combobox(self, width=15)
                    _merc_combobox['values'] = MERC_L_CB
                    _merc_combobox.set(MERC_L[_merc_name])
                    _merc_combobox.pack()
                    _merc_combobox.place(x=0 + _x, y=0 + _y)

                    _level_entry = Entry(self, width=4)
                    _level_entry.insert(0, str(_level))
                    _level_entry.pack()
                    _level_entry.place(x=135 + _x, y=0 + _y)

                    _atk_entry = Entry(self, width=5)
                    _atk_entry.insert(0, str(merc[2]))
                    _atk_entry.pack()
                    _atk_entry.place(x=0 + _x, y=25 + _y)

                    _hp_entry = Entry(self, width=5)
                    _hp_entry.insert(0, str(merc[3]))
                    _hp_entry.pack()
                    _hp_entry.place(x=50 + _x, y=25 + _y)

                    _atk_buff_entry = Entry(self, width=4)
                    _atk_buff_entry.insert(0, str(merc[4]))
                    _atk_buff_entry.pack()
                    _atk_buff_entry.place(x=95 + _x, y=25 + _y)

                    _hp_buff_entry = Entry(self, width=4)
                    _hp_buff_entry.insert(0, str(merc[5]))
                    _hp_buff_entry.pack()
                    _hp_buff_entry.place(x=135 + _x, y=25 + _y)

                    _item_combobox = Combobox(self, width=12)
                    _item_combobox['values'] = ITEM_L_CB_F[_merc_name] + ITEM_L_CB
                    _item_combobox.set(ITEM_L[_item[0]])
                    _item_combobox.pack()
                    _item_combobox.place(x=0 + _x, y=50 + _y)

                    _item_level_combobox = Combobox(self, width=2)
                    _item_level_combobox['values'] = ITEM_LEVEL_CB
                    _item_level_combobox.set(_item[1])
                    _item_level_combobox.pack()
                    _item_level_combobox.place(x=115 + _x, y=50 + _y)

                    _skill_combobox = Combobox(self, width=12)
                    _skill_combobox['values'] = SKILL_L_CB_F[_merc_name] + SKILL_L_CB
                    _skill_combobox.set(SKILL_L[_skill[0]])
                    _skill_combobox.pack()
                    _skill_combobox.place(x=0 + _x, y=75 + _y)

                    _skill_level_combobox = Combobox(self, width=2)
                    _skill_level_combobox['values'] = SKILL_LEVEL_CB
                    _skill_level_combobox.set(_skill[1])
                    _skill_level_combobox.pack()
                    _skill_level_combobox.place(x=115 + _x, y=75 + _y)

                    _skill_target_combobox = Combobox(self, width=2)
                    _skill_target_combobox['values'] = SKILL_TARGET_CB
                    _skill_target_combobox.set(_skill[2])
                    _skill_target_combobox.pack()
                    _skill_target_combobox.place(x=155 + _x, y=75 + _y)

                    _update_button = Button(self, text=MERC_L[_merc_name], width=15)
                    _update_button.pack()
                    if _y == 0:
                        __y = 110
                    else:
                        __y = 715
                    _update_button.place(x=35 + _x, y=__y)
                    _update_button.bind('<Button-1>', self.update_button)
                    _u.append(_update_button)

                    _w.append((_merc_combobox, _level_entry,
                               _atk_entry, _hp_entry, _atk_buff_entry, _hp_buff_entry,
                               _item_combobox, _item_level_combobox,
                               _skill_combobox, _skill_level_combobox, _skill_target_combobox))

                    self.update_merc_image(_c, _i)

                    _i += 1
                    if _i < 7:
                        _swap = Button(self, text='交\n换', width=2)
                        _swap.pack()
                        _swap.place(x=175 + _x, y=20 + _y)
                        _swap.bind('<Button-1>', self.swap_button)
                        _s.append(_swap)

            self.update_canvas()
            # 结算技能 动画 输出日志
            self.log('\n————————\n\n开战！\n')

            for _w, _l in ((self.widgets_1, '\n【敌方】\n'), (self.widgets_2, '\n【己方】\n')):
                self.log(_l)
                for _d in get_info(_w):
                    _m = MERC_L_R[_d[0]]
                    if _m == MERC['-']:
                        continue
                    _log = f'{MERC_L[_m]} {_d[2]}/{_d[3]} ({_d[1]}级 {RACE_L[D[_m][1]]} {M_TYPE_L[D[_m][0]]})\n'
                    self.log(_log)
                    _item = ITEM_L_R[_d[6]]
                    if _item != ITEM['-']:
                        _s = ITEM_D[_item][int(_d[7])]
                        _log = f'　　装备了【{_d[6]}{_d[7]}】。\n　　{_s}\n'
                        self.log(_log)
                    _skill = SKILL_L_R[_d[8]]
                    if _skill != SKILL['-']:
                        _t = SKILL_D[_skill][0]
                        _s, _line, _cd = SKILL_D[_skill][int(_d[9])]
                        _p = f'对【{_d[10]}】号位' if _d[6] != '0' else ''
                        _cd_l = str(_cd) + '回合冷却，' if _cd else ''
                        _log = f'　　{_p}预备【{_d[8]}{_d[9]}】。\n　　{str(_s)}速，{_cd_l}{S_TYPE_L[_t]}属性，{_line}\n'
                        self.log(_log)

            self.log(f'\n手动结算技能，之后开始第{str(self.t)}回合，重新下令。\n')

            self.run_bottum = Button(self, text='下一\n回合', width=5, command=self.run)
            self.run_bottum.pack()
            self.run_bottum.place(x=1460, y=367)

            self._roll_entry = Entry(self, width=4)
            self._roll_entry.insert(0, '2')
            self._roll_entry.pack()
            self._roll_entry.place(x=10, y=325)

            self.roll_bottum = Button(self, text='掷N\n面骰', width=5, command=self.roll)
            self.roll_bottum.pack()
            self.roll_bottum.place(x=10, y=355)

            self.update_bottum = Button(self, text='全部\n刷新', width=5, command=self.update_all)
            self.update_bottum.pack()
            self.update_bottum.place(x=10, y=405)

            self.mainloop()

        def log(self, logs):
            self.parent.log_label.insert(END, logs)
            self.parent.log_label.see(END)

        def update_merc(self, side, pos):
            if side == 'e':
                _widgets = self.widgets_1
                _update = self.widgets_update_1
            else:
                _widgets = self.widgets_2
                _update = self.widgets_update_2

            _name = _widgets[pos][0].get()
            _update[pos].config(text=_name)
            _merc = MERC_L_R[_name]
            _atk, _hp = D[_merc][4][int(_widgets[pos][1].get())]
            _widgets[pos][2].delete(0, END)
            _widgets[pos][2].insert(0, str(_atk))
            _widgets[pos][3].delete(0, END)
            _widgets[pos][3].insert(0, str(_hp))
            _widgets[pos][6]['values'] = ITEM_L_CB_F[_merc] + ITEM_L_CB
            _widgets[pos][8]['values'] = SKILL_L_CB_F[_merc] + SKILL_L_CB

        def update_button(self, event):
            if event.widget in self.widgets_update_1:
                _target = self.widgets_1
                _c = 'e'
                _id = self.widgets_update_1.index(event.widget)
            else:
                _target = self.widgets_2
                _c = 'a'
                _id = self.widgets_update_2.index(event.widget)
            _a = _target[_id][0].get()
            _b = event.widget['text']
            if _a != _b:
                self.update_merc(_c, _id)
            self.update_merc_image(_c, _id)
            self.update_canvas()

        def swap_button(self, event):
            if event.widget in self.widgets_swap_1:
                _target = self.widgets_1
                _c = 'e'
                _id = self.widgets_swap_1.index(event.widget)
                _w = self.widgets_update_1
            else:
                _target = self.widgets_2
                _c = 'a'
                _id = self.widgets_swap_2.index(event.widget)
                _w = self.widgets_update_2
            for i in range(11):
                w_a = _target[_id][i]
                w_b = _target[_id + 1][i]
                _a, _b = w_a.get(), w_b.get()
                if 0 < i < 6:
                    w_a.delete(0, END)
                    w_a.insert(0, _b)
                    w_b.delete(0, END)
                    w_b.insert(0, _a)
                elif i == 6 or i == 8:
                    _aa, _bb = w_a['values'], w_b['values']
                    w_a['values'], w_b['values'] = _bb, _aa
                    w_b.set(_a)
                    w_a.set(_b)
                else:
                    w_b.set(_a)
                    w_a.set(_b)
            _a = _w[_id]['text']
            _b = _w[_id + 1]['text']
            _w[_id].config(text=_b)
            _w[_id + 1].config(text=_a)

            if _target[_id][0].get() != _b:
                self.update_merc(_c, _id)
            if _target[_id + 1][0].get() != _a:
                self.update_merc(_c, _id + 1)
            self.update_merc_image(_c, _id)
            self.update_merc_image(_c, _id + 1)
            self.update_canvas()

        def canvas_press(self, event):
            self.cx, self.cy = event.x, event.y

        def canvas_release(self, event):
            _x1, _y1 = event.x, event.y
            if 0 < _x1 < 1385 and 0 < _y1 < 550:
                _x0, _y0 = self.cx, self.cy
                if _y0 > 275:
                    _color = 'green'
                else:
                    _color = 'red'
                _d2 = pow((_x0 - _x1), 2) + pow((_y0 - _y1), 2)
                if _d2 > 3000:
                    _draw = ImageDraw.ImageDraw(self.canvas_paint)
                    _v1, _v2 = _y0 - _y1, _x1 - _x0
                    _sv = pow(pow(_v1, 2) + pow(_v2, 2), 0.5) / 20
                    _sv2 = _sv / 2
                    _draw.line(((_x0, _y0), (_x1 - int((_x1 - _x0) / _sv2), _y1 - int((_y1 - _y0) / _sv2))
                                ), fill=_color, width=10)

                    _p1 = _x1, _y1
                    _p2 = _x1 + int(_v1 / _sv) - int((_x1 - _x0) / _sv2), _y1 + int(_v2 / _sv) - int((_y1 - _y0) / _sv2)
                    _p3 = _x1 - int(_v1 / _sv) - int((_x1 - _x0) / _sv2), _y1 - int(_v2 / _sv) - int((_y1 - _y0) / _sv2)
                    _draw.polygon((_p1, _p2, _p3), fill=_color, outline=_color)
                    self.update_canvas()

        def update_merc_image(self, side, pos):
            if side == 'e':
                _info = self.widgets_1[pos]
            else:
                _info = self.widgets_2[pos]
            _merc_name = MERC_L_R[_info[0].get()]
            _p = os.path.join('.', 'merc', str(_merc_name.name) + '.png')
            self.merc_img[side][pos] = Image.new('RGBA', (147, 180))
            if _merc_name == MERC['-']:
                pass
            else:
                _draw = ImageDraw.ImageDraw(self.merc_img[side][pos])
                with Image.open(_p) as im:
                    self.merc_img[side][pos].paste(im.convert('RGBA').resize((147, 180), Image.LANCZOS), (0, 0))
                _atk = _info[2].get()
                _atk_int = int(_atk)
                _raw_atk = D[_merc_name][4][int(_info[1].get())][0]
                if _atk_int == _raw_atk:
                    color = 'white'
                elif _atk_int > _raw_atk:
                    color = 'green'
                else:
                    color = 'red'
                _draw.text((30, 150), _atk, color, font, 'mb', align=CENTER,
                           stroke_width=2, stroke_fill='black')
                _hp = _info[3].get()
                _hp_int = int(_hp)
                _raw_hp = D[_merc_name][4][int(_info[1].get())][1]
                if _hp_int == _raw_hp:
                    color = 'white'
                elif _hp_int > _raw_hp:
                    color = 'green'
                else:
                    color = 'red'
                _draw.text((110, 150), _hp, color, font, 'mb', align=CENTER,
                           stroke_width=2, stroke_fill='black')

        def update_params(self):
            global params, M_SET
            new_e = []
            new_a = []
            for new_ae, old_ae in ((new_e, self.widgets_1), (new_a, self.widgets_2)):
                ele = get_info(old_ae)
                for e in ele:
                    _merc = MERC_L_R[e[0]]
                    if _merc == MERC['-']:
                        new_ae.append(M_SET[0])
                    else:
                        new_ae.append((_merc, int(e[1]), int(e[2]), int(e[3]), int(e[4]), int(e[5]), (
                            ITEM_L_R[e[6]], int(e[7])), (SKILL_L_R[e[8]], int(e[9]), int(e[10])), ()))
            params = {
                'w': self.winfo_width(),
                'h': self.winfo_height(),
                'x': self.winfo_x(),
                'y': self.winfo_y() + 30,
                't': self.t + 1,
                'e': new_e,
                'a': new_a,
            }

        def roll(self):
            num = self._roll_entry.get()
            _ro = randint(1, int(num))
            self.log(f'从1到{num}的随机整数：{str(_ro)}\n')

        def update_canvas(self):
            _im = self.canvas_img.copy()
            for _c in ('e', 'a'):
                for _i in range(7):
                    _x = 205 * _i + 4
                    _y = 50 if _c == 'e' else 320
                    _im.paste(self.merc_img[_c][_i], (_x, _y, _x + 147, _y + 180), self.merc_img[_c][_i])
            _im.paste(self.canvas_paint, mask=self.canvas_paint)
            self.canvas_imgp = ImageTk.PhotoImage(_im)
            self.canvas.create_image((0, 0), image=self.canvas_imgp, anchor=NW)

        def update_all(self):
            for _c, _t, _u in (('e', self.widgets_1, self.widgets_update_1),
                               ('a', self.widgets_2, self.widgets_update_2)):
                for _id in range(7):
                    _a = _t[_id][0].get()
                    _b = _u[_id]['text']
                    if _a != _b:
                        self.update_merc(_c, _id)
                    self.update_merc_image(_c, _id)
            self.canvas_paint = Image.new('RGBA', (1385, 550))
            self.update_canvas()

        def run(self):
            self.update_params()
            MainWindow.SideWindow()

    def __init__(self):
        super().__init__()
        self.title('佣兵沙盘')
        self.w = 400
        self.h = 800
        self.x = 10
        self.y = 80
        with Image.open('background.png') as _im:
            _size = (params['w'], params['h'])
            _imm = Image.new('RGBA', _size)
            _imm.paste(_im.convert('RGBA').resize(_size, Image.LANCZOS), (0, 0))
            _imp = ImageTk.PhotoImage(_imm)
            self.bgimg = _imp
        self.geometry(f'{str(self.w)}x{str(self.h)}+{str(self.x)}+{str(self.y)}')
        self.log = StringVar(
            value='欢迎使用佣兵沙盘DEMO。\n数值不完整，某些操作会报错。\n切技能换目标不需要点更新英雄。\n更新英雄会同刷新图片。未来可能补自'
                  '动结算。\n日志可擦除。\n在棋盘上拖动会画箭头，下面起点为绿色，上面起点为红色，左侧全部刷新擦除箭头。\n每个佣兵的控件依次对'
                  '应：\n【名称】【等级】\n【攻击力】【生命值】\n【装备】【等级】\n【技能】【等级】【目标】\n'
        )
        self.log_label = Text(self)
        self.log_label.insert(END, self.log.get())
        self.log_label.pack(expand=1, fill=BOTH)
        self.SideWindow()
        self.mainloop()


if __name__ == '__main__':
    main = MainWindow()
