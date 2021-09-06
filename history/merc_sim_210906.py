from tkinter import *
from tkinter.ttk import *
from enum import Enum
from PIL import Image, ImageTk, ImageChops  # ImageGrab
import os
import ctypes
# import random
#
# g_s = ctypes.windll.user32.GetSystemMetrics
# screensize = g_s(78), g_s(79)

MERC = Enum('MERC', (
    '-',
    'Cariel Roame',
    'Tyrande',
    'Xyrella',
    'Rokara',
))
MERC_L = {
    MERC['-']: '----',
    MERC['Cariel Roame']: '凯瑞尔·罗姆',
    MERC['Tyrande']: '泰兰德',
    MERC['Xyrella']: '泽瑞拉',
    MERC['Rokara']: '洛卡拉',
}
MERC_L_R = dict(zip(MERC_L.values(), MERC_L.keys()))
MERC_L_CB = tuple(MERC_L.values())

RACE = Enum('RACE',
            ('-', 'Tauren', 'Human', 'Orc', 'Beast', 'Demon', 'Murloc', 'Element', 'Night Elf', 'Gnome', 'Undead',
             'Dwarf', 'Blood Elf', 'Troll', 'High Elf', 'Dragon', 'Draenei'))
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
    RACE['High Elf']: '高等精灵',
    RACE['Dragon']: '龙',
    RACE['Draenei']: '德莱尼',
}
M_TYPE = Enum('M_TYPE', ('-', 'Protector', 'Fighter', 'Caster'))
M_TYPE_L = {
    M_TYPE['-']: '无业',
    M_TYPE['Protector']: '护卫',
    M_TYPE['Fighter']: '斗士',
    M_TYPE['Caster']: '施法者',
}
S_TYPE = Enum('S_TYPE', ('-', 'Holy', 'Arcane'))
S_TYPE_L = {
    S_TYPE['-']: '无',
    S_TYPE['Holy']: '神圣',
    S_TYPE['Arcane']: '奥术',
}
SKILL = Enum('SKILL', (
    '-',
    # Cariel Roame
    "Crusader's Blow",
    'Taunt',
    'Seal of Light',
    # Tyrande
    'Arcane Shot',
    'Arcane Salvo',
    "Elune's Grace",
    # Xyrella
    'Blinding Luminance',
    'Flash Heal',
    'Atonement',
))
SKILL_L = {
    SKILL['-']: '休息',
    SKILL["Crusader's Blow"]: '远征军打击',
    SKILL['Taunt']: '嘲讽',
    SKILL['Seal of Light']: '光明圣印',
    SKILL['Arcane Shot']: '奥术射击',
    SKILL['Arcane Salvo']: '奥术齐射',
    SKILL["Elune's Grace"]: '艾露恩的赐福',
    SKILL['Blinding Luminance']: '致盲之光',
    SKILL['Flash Heal']: '快速治疗',
    SKILL['Atonement']: '救赎',
}
SKILL_L_R = dict(zip(SKILL_L.values(), SKILL_L.keys()))
SKILL_L_CB = tuple(SKILL_L.values())

SKILL_D = {
    SKILL['-']: [S_TYPE['-']] + [(114, '为什么佣兵战纪不能休息？')] * 5,
    SKILL["Crusader's Blow"]: [S_TYPE['Holy']] + [(6, '攻击一个敌人。击杀：为此佣兵恢复10点生命值。')] * 5,
    SKILL['Taunt']: [S_TYPE['-']] + [(1, '为此佣兵恢复4点生命值，并使其在本回合中获得嘲讽。')] * 5,
    SKILL['Seal of Light']: [S_TYPE['Holy']] + [(4, '选择一个角色，使其获得+2攻击力并为其恢复5点生命值。')] * 5,
    SKILL['Arcane Shot']: [S_TYPE['Arcane']] + [(7, '对一个敌人造成4点伤害。')] * 5,
    SKILL['Arcane Salvo']: [S_TYPE['Arcane']] + [(5, '随机对两个敌人造成2点伤害。')] * 5,
    SKILL["Elune's Grace"]: [S_TYPE['Arcane']] + [(6, '你的队伍的下一个奥术技能会施放两次，且速度值永久加快（1）点。')] * 5,
    SKILL['Blinding Luminance']: [S_TYPE['Holy']] + [(3, '对一个敌人造成2点伤害，并使其在本回合获得-2攻击力。')] * 5,
    SKILL['Flash Heal']: [S_TYPE['Holy']] + [(4, '恢复5点生命值。')] * 5,
    SKILL['Atonement']: [S_TYPE['Holy']] + [(9, '造成9点伤害。你的队伍每恢复20点生命值，伤害+1。')] * 5,
}

SKILL_LEVEL_CB = (1, 2, 3, 4, 5)
SKILL_TARGET_CB = (0, 1, 2, 3, 4, 5, 6, 7, -1, -2, -3, -4, -5, -6, -7)

ITEM = Enum('ITEM', (
    '-',
    'Hammer of Dawn',
    'Tome of Light',
    'Tome of Judgement',
))
ITEM_L = {
    ITEM['-']: '无装备',
    ITEM['Hammer of Dawn']: '黎明之锤',
    ITEM['Tome of Light']: '圣光秘典',
    ITEM['Tome of Judgement']: '裁决秘典',
}
ITEM_L_R = dict(zip(ITEM_L.values(), ITEM_L.keys()))
ITEM_L_CB = tuple(ITEM_L.values())
ITEM_D = {
    ITEM['-']: ['没有装备。'] * 5,
    ITEM['Hammer of Dawn']: ['远征军打击还会为相邻的佣兵恢复生命值。'] * 5,
    ITEM['Tome of Light']: ['被动：当此佣兵具有嘲讽时，具有+2攻击力。'] * 5,
    ITEM['Tome of Judgement']: ['光明圣印额外使目标获得+1攻击力。'] * 5,
}
ITEM_LEVEL_CB = (1, 2, 3, 4)
D = {
    MERC['-']: (M_TYPE['-'], RACE['-'], (SKILL['-'],), (), (
        (0, 0), (0, 0),
    )),
    MERC['Cariel Roame']: (M_TYPE['Protector'], RACE['Human'], (
        ITEM['Hammer of Dawn'], ITEM['Tome of Light'], ITEM['Tome of Judgement']), (
                               SKILL["Crusader's Blow"], SKILL['Taunt'], SKILL['Seal of Light']), (
                               (3, 10), (3, 10),
                           )),
    MERC['Tyrande']: (M_TYPE['Fighter'], RACE['Night Elf'], (ITEM['-'], 1), (SKILL['Arcane Shot'],), (
        (1, 9), (1, 9),
    )),
    MERC['Xyrella']: (M_TYPE['Caster'], RACE['Draenei'], (ITEM['-'], 1), (SKILL['Blinding Luminance'],), (
        (1, 7), (1, 7),
    )),
    MERC['Rokara']: (M_TYPE['Fighter'], RACE['Orc'], (ITEM['-'], 1), (SKILL['Arcane Shot'],), (
        (2, 11), (2, 11),
    ))}
L = 1  # 初始等级
M_SET = [(MERC[n], L, D[MERC[n]][4][L][0], D[MERC[n]][4][L][1], (ITEM['-'], 1), (SKILL['-'], 1, 0), ()) for n in (
    '-', 'Cariel Roame', 'Tyrande', 'Xyrella')]
params = {
    'w': 1430,
    'h': 700,
    'x': 50,
    'y': 50,
    't': 1,
    'e': [M_SET[0], M_SET[1], M_SET[0], M_SET[2], M_SET[0], M_SET[3], M_SET[0]],
    'a': [M_SET[0], M_SET[1], M_SET[0], M_SET[2], M_SET[0], M_SET[3], M_SET[0]]
}


class MainWindow(Tk):
    class SideWindow(Toplevel):
        def __init__(self):
            super().__init__()
            self.parent = self.nametowidget(self.winfo_parent())
            self.t = params['t']
            self.title(f'第{str(self.t)}回合')
            self.w = params['w']
            self.h = params['h']
            self.x = params['x']
            self.y = params['y']
            self.geometry(f'{str(self.w)}x{str(self.h)}+{str(self.x)}+{str(self.y)}')
            self.resizable(False, False)
            self.bg = Canvas(self, width=960, height=490)
            self.bg.grid(row=4, column=1, rowspan=3, columnspan=34, sticky=NSEW)
            self.dd = ImageTk.PhotoImage(self.parent.bgimg)
            self.bg.create_image((0, 0), anchor=NW, image=self.dd)

            self.m1 = Canvas(self, width=100, height=100)
            self.m1.grid(row=0, column=0, columnspan=5, sticky=NSEW)
            with Image.open('merc/1.png') as _im:
                self.d1 = Image.new('RGBA', _im.size)
                self.d1.paste(_im.convert('RGBA'), (0, 0))
            self.dd = ImageTk.PhotoImage(self.d1)
            self.m1.create_image((0, 0), anchor=NW, image=self.dd)

            self.widgets_1 = []
            self.widgets_swap_1 = []
            self.widgets_2 = []
            self.widgets_swap_2 = []

            for _c, _w, _s, _r, _t in (('e', self.widgets_1, self.widgets_swap_1, 0, NW),
                                       ('a', self.widgets_1, self.widgets_swap_2, 5, SW)):
                _i = 0
                for merc in params[_c]:
                    _merc_name = merc[0]
                    _level = merc[1]
                    _item = merc[4]
                    if not _item:
                        _item = (ITEM['-'], 1, 0)
                    _skill = merc[5]
                    if not _skill:
                        _skill = (SKILL['-'], 1, 0)
                    _passive = merc[6]

                    _merc_combobox = Combobox(self, width=16)
                    _merc_combobox['values'] = MERC_L_CB
                    _merc_combobox.set(MERC_L[_merc_name])
                    _merc_combobox.grid(row=_r + 0, column=0 + _i * 5, columnspan=3, sticky=_t)

                    _level_entry = Entry(self, width=5)
                    _level_entry.insert(0, str(merc[1]))
                    _level_entry.grid(row=_r + 0, column=3 + _i * 5, sticky=_t)

                    _atk_entry = Entry(self, width=5)
                    _atk_entry.insert(0, str(merc[2]))
                    _atk_entry.grid(row=_r + 1, column=0 + _i * 5, sticky=_t)

                    _hp_entry = Entry(self, width=5)
                    _hp_entry.insert(0, str(merc[3]))
                    _hp_entry.grid(row=_r + 1, column=1 + _i * 5, sticky=_t)

                    _atk_buff_entry = Entry(self, width=5)
                    _atk_buff_entry.insert(0, '0')
                    _atk_buff_entry.grid(row=_r + 1, column=2 + _i * 5, sticky=_t)

                    _hp_buff_entry = Entry(self, width=5)
                    _hp_buff_entry.insert(0, '0')
                    _hp_buff_entry.grid(row=_r + 1, column=3 + _i * 5, sticky=_t)

                    _item_combobox = Combobox(self, width=10)
                    _item_combobox['values'] = ITEM_L_CB
                    _item_combobox.set(ITEM_L[_item[0]])
                    _item_combobox.grid(row=_r + 2, column=0 + _i * 5, columnspan=2, sticky=_t)

                    _item_level_combobox = Combobox(self, width=3)
                    _item_level_combobox['values'] = ITEM_LEVEL_CB
                    _item_level_combobox.set(_item[1])
                    _item_level_combobox.grid(row=_r + 2, column=2 + _i * 5, sticky=_t)

                    _skill_combobox = Combobox(self, width=10)
                    _skill_combobox['values'] = SKILL_L_CB
                    _skill_combobox.set(SKILL_L[_skill[0]])
                    _skill_combobox.grid(row=_r + 3, column=0 + _i * 5, columnspan=2, sticky=_t)

                    _skill_level_combobox = Combobox(self, width=3)
                    _skill_level_combobox['values'] = SKILL_LEVEL_CB
                    _skill_level_combobox.set(_skill[1])
                    _skill_level_combobox.grid(row=_r + 3, column=2 + _i * 5, sticky=_t)

                    _skill_target_combobox = Combobox(self, width=3)
                    _skill_target_combobox['values'] = SKILL_TARGET_CB
                    _skill_target_combobox.set(_skill[2])
                    _skill_target_combobox.grid(row=_r + 3, column=3 + _i * 5, sticky=_t)

                    _w.append((_merc_combobox, _level_entry,
                               _atk_entry, _hp_entry, _atk_buff_entry, _hp_buff_entry,
                               _item_combobox, _item_level_combobox,
                               _skill_combobox, _skill_level_combobox, _skill_target_combobox,))

                    if _i < 6:
                        _swap = Button(self, text='交\n换', width=2)
                        _swap.grid(row=_r + 0, column=4 + _i * 5, rowspan=4, sticky=W)
                        _s.append(_swap)
                    _i += 1

            # 结算技能 动画 输出日志
            self.log('\n————————\n\n开战！\n\n【敌方】\n')
            #
            # for e in self.widgets_1:
            #     _d = e[2].get(), e[3].get(), e[4].get(), e[5].get(), e[6].get(), e[7].get(), e[8].get()
            #     _m = MERC_L_R[_d[0]]
            #     if _m == MERC['-']:
            #         continue
            #     _log = f'({_d[1]}级 {RACE_L[D[_m][1]]} {M_TYPE_L[D[_m][0]]}) {MERC_L[_m]} 属性：{_d[2]}/{_d[3]}\n'
            #     self.log(_log)
            #     _skill = SKILL_L_R[_d[4]]
            #     if _skill != SKILL['-']:
            #         _t = SKILL_D[_skill][0]
            #         _s, _line = SKILL_D[_skill][int(_d[5])]
            #         _p = f'对【{_d[6]}】号位' if _d[6] != '0' else ''
            #         _log = f'　　{_p}预备【{_d[4]}{_d[5]}】。\n　　{str(_s)}速，{S_TYPE_L[_t]}属性，{_line}\n'
            #         self.log(_log)
            #
            # self.log('\n【己方】\n')
            #
            # for e in self.widgets_2:
            #     _d = e[2].get(), e[3].get(), e[4].get(), e[5].get(), e[6].get(), e[7].get(), e[8].get()
            #     _m = MERC_L_R[_d[0]]
            #     if _m == MERC['-']:
            #         continue
            #     _log = f'({_d[1]}级 {RACE_L[D[_m][1]]} {M_TYPE_L[D[_m][0]]}){MERC_L[_m]} 属性：{_d[2]}/{_d[3]}\n'
            #     self.log(_log)
            #     _skill = SKILL_L_R[_d[4]]
            #     if _skill != SKILL['-']:
            #         _t = SKILL_D[_skill][0]
            #         _s, _line = SKILL_D[_skill][int(_d[5])]
            #         _p = f'对【{_d[6]}】号位' if _d[6] != '0' else ''
            #         _log = f'　　{_p}预备【{_d[4]}{_d[5]}】。\n　　{str(_s)}速，{S_TYPE_L[_t]}属性，{_line}\n'
            #         self.log(_log)

            self.log(f'\n手动结算，之后开始第{str(self.t)}回合。\n')

            # self.run_bottum = Button(self, text='下一回合', width=13, command=self.run)
            # self.run_bottum.pack()
            # self.run_bottum.place(x=0, y=310)
            #
            # self.update_bottum = Button(self, text='更新英雄&技能', width=14, command=self._update)
            # self.update_bottum.pack()
            # self.update_bottum.place(x=150, y=310)
            #
            # self._roll_entry = Entry(self, width=3)
            # self._roll_entry.insert(0, '2')
            # self._roll_entry.pack()
            # self._roll_entry.place(x=400, y=310)
            #
            # self.roll_bottum = Button(self, text='掷骰', width=10, command=self.roll)
            # self.roll_bottum.pack()
            # self.roll_bottum.place(x=300, y=310)

            self.mainloop()

        def log(self, logs):
            self.parent.log_label.insert(END, logs)
            self.parent.log_label.see(END)

        def update_merc_image(self, _lable: Widget, _merc_name):
            _p = os.path.join('.', 'merc', str(_merc_name.value) + '.png')
            with Image.open(_p) as im:
                _image = Image.new('RGBA', (150, 180))
                _image.paste(im.convert('RGBA').resize((150, 180), Image.LANCZOS), (0, 0))
                _image_done = ImageTk.PhotoImage(_image)
                _lable.configure(image=_image_done)
                _lable.image = _image_done

        def update_skill_image(self, _lable: Widget, _skill_name):
            _p = os.path.join('.', 'skill', str(_skill_name.value) + '.png')
            with Image.open(_p) as im:
                _image = Image.new('RGBA', (70, 100))
                _image.paste(im.convert('RGBA').resize((70, 100), Image.LANCZOS), (0, 0))
                _image_done = ImageTk.PhotoImage(_image)
                _lable.configure(image=_image_done)
                _lable.image = _image_done

        def update_params(self):
            global params
            new_e = []
            new_a = []
            for new_ae, old_ae in ((new_e, self.widgets_1), (new_a, self.widgets_2)):
                ele = self.get_f2(old_ae)
                i = 0
                for e in ele:
                    _merc = MERC_L_R[e[0]]
                    if _merc == MERC['-']:
                        continue
                    new_ae.append((_merc, int(e[1]), int(e[2]), int(e[3]), (
                        SKILL_L_R[e[4]], int(e[5]), int(e[6])), (), ()))
                    i += 1
                while i < 3:
                    new_ae.append((MERC['-'], L, 0, 0, (), (), ()))
                    i += 1

            params = {
                'w': self.winfo_width(),
                'h': self.winfo_height(),
                'x': min(self.winfo_x() + self.winfo_width(), screensize[0] - self.winfo_width()),  # 忽略多屏DPI不同的问题
                'y': self.winfo_y(),
                't': self.t + 1,
                'e': new_e,
                'a': new_a,
            }

        def get_f1(self, af_ef):
            return [(e[0]['text'], e[2].get(), e[3].get(), e[4].get(), e[5].get(), e[6].get()) for e in af_ef]

        def get_f2(self, af_ef):
            return [(e[2].get(), e[3].get(), e[4].get(), e[5].get(), e[6].get(), e[7].get(), e[8].get()) for e in af_ef]

        def roll(self):
            num = self._roll_entry.get()
            _ro = random.randint(1, int(num))
            self.log(f'1到{num}随机数：{str(_ro)}\n')

        def _update(self):
            for af_ef in (self.widgets_2, self.widgets_1):
                old_f = self.get_f1(af_ef)
                i = 0
                for e in old_f:
                    if e[0] != e[1]:
                        af_ef[i][0]['text'] = e[1]
                        self.update_merc_image(af_ef[i][1], MERC_L_R[e[1]])
                        _l = int(e[2])
                        _m = MERC_L_R[e[1]]
                        af_ef[i][4].delete(0, END)
                        af_ef[i][4].insert(0, str(D[_m][4][_l][0]))
                        af_ef[i][5].delete(0, END)
                        af_ef[i][5].insert(0, str(D[_m][4][_l][1]))
                    self.update_skill_image(af_ef[i][9], SKILL_L_R[e[5]])
                    i += 1

        def run(self):
            self.update_params()
            MainWindow.SideWindow()

    def __init__(self):
        super().__init__()
        self.title('佣兵沙盘')
        # 主窗口放使用教程
        self.w = 600
        self.h = 400
        self.x = 80
        self.y = 80
        with Image.open('background.png') as _im:
            self.bgimg = Image.new('RGBA', _im.size)
            self.bgimg.paste(_im.convert('RGBA'), (0, 0))
        self.geometry(f'{str(self.w)}x{str(self.h)}+{str(self.x)}+{str(self.y)}')
        self.log = StringVar(value='欢迎使用佣兵沙盘DEMO。\n数值不完整，某些操作会报错。\n'
                                   '切技能换目标不需要点更新英雄。\n更新英雄会同刷新图片。未来可能补自动结算。\n日志可擦除。\n')
        self.log_label = Text(self)
        self.log_label.insert(END, self.log.get())
        self.log_label.pack(expand=1, fill=BOTH)

        self.SideWindow()

        self.mainloop()


if __name__ == '__main__':
    main = MainWindow()
