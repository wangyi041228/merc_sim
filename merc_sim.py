from tkinter import *
from tkinter.ttk import *
from enum import Enum
from PIL import Image, ImageTk  # ImageGrab, ImageChops
import os
import ctypes

g_s = ctypes.windll.user32.GetSystemMetrics
screensize = g_s(78), g_s(79)

MERC = Enum('MERC', (
    'None',
    'Cariel Roame',
    'Tyrande',
    'Xyrella',
    'Rokara',
))
MERC_L = {
    MERC['None']: '留空',
    MERC['Cariel Roame']: '凯瑞尔·罗姆',
    MERC['Tyrande']: '泰兰德',
    MERC['Xyrella']: '泽瑞拉',
    MERC['Rokara']: '洛卡拉',
}
MERC_L_R = dict(zip(MERC_L.values(), MERC_L.keys()))
MERC_L_CB = tuple(MERC_L.values())

RACE = Enum('RACE', ('None', 'Tauren', 'Human', 'Orc', 'Beast', 'Demon', 'Murloc', 'Element', 'Night Elf', 'Gnome', 'Undead',
                     'Dwarf', 'Blood Elf', 'Troll', 'High Elf', 'Dragon', 'Draenei'))
M_TYPE = Enum('M_TYPE', 'Protector Fighter Caster')
SKILL = Enum('SKILL', (
    'None',
    "Crusader's Blow",
    'Arcane Shot',
    'Blinding Luminance',
))
SKILL_L = {
    SKILL['None']: '留空',
    SKILL["Crusader's Blow"]: '远征军打击',
    SKILL['Arcane Shot']: '奥术齐射',
    SKILL['Blinding Luminance']: '致盲之光',
}
SKILL_L_R = dict(zip(SKILL_L.values(), SKILL_L.keys()))
SKILL_L_CB = tuple(SKILL_L.values())
SKILL_LEVEL_CB = (1, 2, 3, 4, 5)
SKILL_TARGET_CB = (0, 1, 2, 3, 4, 5, 6, 7, -1, -2, -3, -4, -5, -6, -7)

ITEM = Enum('ITEM', (
    'A',
    'B',
    'C',
))

D = {
    MERC['None']: (M_TYPE['Protector'], RACE['None'], (), (), (
        (0, 0), (0, 0),
    )),
    MERC['Cariel Roame']: (M_TYPE['Protector'], RACE['Human'], (SKILL["Crusader's Blow"],), (ITEM['A'],), (
        (3, 10), (3, 10),
    )),
    MERC['Tyrande']: (M_TYPE['Fighter'], RACE['Night Elf'], (SKILL['Arcane Shot'],), (ITEM['B'],), (
        (2, 11), (2, 11),
    )),
    MERC['Xyrella']: (M_TYPE['Caster'], RACE['Draenei'], (SKILL['Blinding Luminance'],), (ITEM['C'],), (
        (1, 7), (1, 7),
    )),
    MERC['Rokara']: (M_TYPE['Fighter'], RACE['Orc'], (SKILL['Arcane Shot'],), (ITEM['B'],), (
        (2, 11), (2, 11),
    ))}
L = 1  # 初始等级
params = {
    'w': 690,
    'h': 650,
    'x': 50,
    'y': 50,
    't': 1,
    'e': [(MERC[n], L, D[MERC[n]][4][L][0], D[MERC[n]][4][L][1], (), (), ()) for n in (
        'Cariel Roame', 'Tyrande', 'Xyrella')],
    'a': [(MERC[n], L, D[MERC[n]][4][L][0], D[MERC[n]][4][L][1], (), (), ()) for n in (
        'Cariel Roame', 'Tyrande', 'Xyrella')]
}


class MainWindow(Tk):
    class SideWindow(Toplevel):
        def __init__(self):
            super().__init__()
            self.t = params['t']
            self.title(f'第{str(self.t)}回合')
            self.w = params['w']
            self.h = params['h']
            self.x = params['x']
            self.y = params['y']
            self.geometry(f'{str(self.w)}x{str(self.h)}+{str(self.x)}+{str(self.y)}')
            self.run_bottum = Button(self, text='下一回合', width=13, command=self.run)
            self.run_bottum.pack()
            self.run_bottum.place(x=0, y=310)

            self.update_bottum = Button(self, text='更新英雄&技能', width=14, command=self._update)
            self.update_bottum.pack()
            self.update_bottum.place(x=150, y=310)

            self.e = params['e']
            self.ef = []
            self.a = params['a']
            self.af = []

            # 结算技能，更新数值
            this_log = '\n新一回合'
            parent = self.nametowidget(self.winfo_parent())
            parent.log_label.insert(END, this_log)
            parent.log_label.see(END)

            i = 0
            for merc in self.e:
                # (佣兵, 等级, 攻击力, 生命值, 选中技能, 使用装备, 被动)
                _merc_name = merc[0]
                if _merc_name == MERC['None']:
                    continue

                _level = merc[1]
                _skill = merc[4]
                if not _skill:
                    _skill = (SKILL['None'], 1, 0)
                _item = merc[5]
                _passive = merc[6]

                _lable_frame = LabelFrame(self, text=MERC_L[merc[0]], height=300, width=220)
                _lable_frame.pack()
                _lable_frame.place(x=i * 230, y=0)

                _image_lable = Label(_lable_frame)
                _image_lable.pack()
                _image_lable.place(x=0, y=100)
                self.update_merc_image(_image_lable, _merc_name)

                _merc_combobox = Combobox(_lable_frame)
                _merc_combobox['values'] = MERC_L_CB
                _merc_combobox.set(MERC_L[_merc_name])
                _merc_combobox.pack()
                _merc_combobox.place(x=0, y=200)

                _level_entry = Entry(_lable_frame, width=3)
                _level_entry.insert(0, str(merc[1]))
                _level_entry.pack()
                _level_entry.place(x=60, y=255)

                _atk_entry = Entry(_lable_frame, width=4)
                _atk_entry.insert(0, str(merc[2]))
                _atk_entry.pack()
                _atk_entry.place(x=20, y=230)

                _hp_entry = Entry(_lable_frame, width=4)
                _hp_entry.insert(0, str(merc[3]))
                _hp_entry.pack()
                _hp_entry.place(x=105, y=230)

                _skill_combobox = Combobox(_lable_frame)
                _skill_combobox['values'] = SKILL_L_CB
                _skill_combobox.set(SKILL_L[_skill[0]])
                _skill_combobox.pack()
                _skill_combobox.place(x=90, y=0, width=90)

                _skill_level_combobox = Combobox(_lable_frame)
                _skill_level_combobox['values'] = SKILL_LEVEL_CB
                _skill_level_combobox.set(_skill[1])
                _skill_level_combobox.pack()
                _skill_level_combobox.place(x=90, y=30, width=90)

                _skill_target_combobox = Combobox(_lable_frame)
                _skill_target_combobox['values'] = SKILL_TARGET_CB
                _skill_target_combobox.set(_skill[2])
                _skill_target_combobox.pack()
                _skill_target_combobox.place(x=90, y=60, width=90)

                _skill_image_lable = Label(_lable_frame)
                _skill_image_lable.pack()
                _skill_image_lable.place(x=10, y=0)
                self.update_skill_image(_skill_image_lable, _skill[0])

                self.ef.append((_lable_frame, _image_lable, _merc_combobox, _level_entry, _atk_entry, _hp_entry,
                                _skill_combobox, _skill_level_combobox, _skill_target_combobox, _skill_image_lable))
                i += 1

            i = 0
            for merc in self.a:
                # (佣兵, 等级, 攻击力, 生命值, 选中技能, 使用装备, 被动)
                _merc_name = merc[0]
                if _merc_name == MERC['None']:
                    continue

                _level = merc[1]
                _skill = merc[4]
                if not _skill:
                    _skill = (SKILL['None'], 1, 0)
                _item = merc[5]
                _passive = merc[6]

                _lable_frame = LabelFrame(self, text=MERC_L[merc[0]], height=300, width=220)
                _lable_frame.pack()
                _lable_frame.place(x=i * 230, y=340)

                _image_lable = Label(_lable_frame)
                _image_lable.pack()
                _image_lable.place(x=0, y=0)
                self.update_merc_image(_image_lable, _merc_name)

                _merc_combobox = Combobox(_lable_frame)
                _merc_combobox['values'] = MERC_L_CB
                _merc_combobox.set(MERC_L[_merc_name])
                _merc_combobox.pack()
                _merc_combobox.place(x=0, y=100)

                _level_entry = Entry(_lable_frame, width=3)
                _level_entry.insert(0, str(merc[1]))
                _level_entry.pack()
                _level_entry.place(x=60, y=155)

                _atk_entry = Entry(_lable_frame, width=4)
                _atk_entry.insert(0, str(merc[2]))
                _atk_entry.pack()
                _atk_entry.place(x=20, y=130)

                _hp_entry = Entry(_lable_frame, width=4)
                _hp_entry.insert(0, str(merc[3]))
                _hp_entry.pack()
                _hp_entry.place(x=105, y=130)

                _skill_combobox = Combobox(_lable_frame)
                _skill_combobox['values'] = SKILL_L_CB
                _skill_combobox.set(SKILL_L[_skill[0]])
                _skill_combobox.pack()
                _skill_combobox.place(x=90, y=190, width=90)

                _skill_level_combobox = Combobox(_lable_frame)
                _skill_level_combobox['values'] = SKILL_LEVEL_CB
                _skill_level_combobox.set(_skill[1])
                _skill_level_combobox.pack()
                _skill_level_combobox.place(x=90, y=220, width=90)

                _skill_target_combobox = Combobox(_lable_frame)
                _skill_target_combobox['values'] = SKILL_TARGET_CB
                _skill_target_combobox.set(_skill[2])
                _skill_target_combobox.pack()
                _skill_target_combobox.place(x=90, y=250, width=90)

                _skill_image_lable = Label(_lable_frame)
                _skill_image_lable.pack()
                _skill_image_lable.place(x=10, y=190)
                self.update_skill_image(_skill_image_lable, _skill[0])

                self.af.append((_lable_frame, _image_lable, _merc_combobox, _level_entry, _atk_entry, _hp_entry,
                                _skill_combobox, _skill_level_combobox, _skill_target_combobox, _skill_image_lable))
                i += 1

            self.mainloop()

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
            for new_ae, old_ae in ((new_e, self.ef), (new_a, self.af)):
                ele = self.get_f2(old_ae)
                i = 0
                for e in ele:
                    if e[0] == MERC['None']:
                        continue
                    new_ae.append((MERC_L_R[e[0]], int(e[1]), int(e[2]), int(e[3]), (
                        SKILL_L_R[e[4]], int(e[5]), int(e[6])), (), ()))
                    i += 1
                while i < 3:
                    new_ae.append((MERC['None'], L, 0, 0, (), (), ()))
                    i += 1

            params = {
                'w': self.winfo_width(),
                'h': self.winfo_height(),
                'x': min(self.winfo_x() + 100, screensize[0] - self.winfo_width()),  # 忽略多屏DPI不同的问题
                'y': self.winfo_y(),
                't': self.t + 1,
                'e': new_e,
                'a': new_a,
            }

        def get_f1(self, af_ef):
            return [(e[0]['text'], e[2].get(), e[3].get(), e[4].get(), e[5].get(), e[6].get()) for e in af_ef]

        def get_f2(self, af_ef):
            return [(e[2].get(), e[3].get(), e[4].get(), e[5].get(), e[6].get(), e[7].get(), e[8].get()) for e in af_ef]

        def _update(self):
            for af_ef in (self.af, self.ef):
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
        self.title('佣兵模拟器')
        # 主窗口放使用教程
        self.w = 250
        self.h = 200
        self.x = 50
        self.y = 800
        self.geometry(f'{str(self.w)}x{str(self.h)}+{str(self.x)}+{str(self.y)}')
        self.log = StringVar(value='欢迎使用佣兵模拟器DEMO。数值不完整，某些操作会引发错误。'
                                   '切技能换目标不需要点更新英雄。更新英雄会同刷新图片。')
        self.log_label = Text(self)
        self.log_label.insert(END, self.log.get())
        self.log_label.pack(fill=BOTH)

        self.SideWindow()

        self.mainloop()


if __name__ == '__main__':
    main = MainWindow()
