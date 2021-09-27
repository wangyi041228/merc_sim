from PIL import Image, ImageDraw, ImageFont
import math
import os
from enum import Enum
from json import loads

with open('data_skill.json', 'r', encoding='utf-8') as _f_:
    d_skill = loads(_f_.read())
with open('data_item.json', 'r', encoding='utf-8') as _f_:
    d_item = loads(_f_.read())
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
    ITEM_D[ITEM[d_item[0][_count]]] = [m_l - 1, d_item[2][_count], d_item[3][_count], d_item[4][_count],
                                       d_item[5][_count]]
ITEM_L_R = dict(zip(ITEM_L.values(), ITEM_L.keys()))
ITEM_L_CB = d_item[1]
ITEM_L_CB_F = {}
ITEM_LEVEL_CB = (1, 2, 3, 4)

font_1_p = os.sep.join(('font', 'GLEI00M_t.ttf'))
font_2_p = os.sep.join(('font', 'BlizzardGlobal-Bold.ttf'))  # 暴黑加粗
font_2b_p = os.sep.join(('font', 'BlizzardGlobal-Bold.ttf'))  # 暴黑加粗 还没加粗
font_1_21 = ImageFont.truetype(font=font_1_p, size=21, index=0)
font_1_22 = ImageFont.truetype(font=font_1_p, size=22, index=0)
font_1_24 = ImageFont.truetype(font=font_1_p, size=24, index=0)
font_1_26 = ImageFont.truetype(font=font_1_p, size=26, index=0)  # （备用）缩小牌名
font_1_28 = ImageFont.truetype(font=font_1_p, size=28, index=0)
font_1_32 = ImageFont.truetype(font=font_1_p, size=32, index=0)  # 类别标签
font_1_34 = ImageFont.truetype(font=font_1_p, size=34, index=0)  # 标准牌名
font_1_106 = ImageFont.truetype(font=font_1_p, size=106, index=0)  # 攻击力 生命值
font_1_116 = ImageFont.truetype(font=font_1_p, size=116, index=0)  # 费用

font_2_14 = ImageFont.truetype(font=font_2_p, size=14, index=0)
font_2b_14 = ImageFont.truetype(font=font_2b_p, size=14, index=0)
font_2_16 = ImageFont.truetype(font=font_2_p, size=16, index=0)
font_2b_16 = ImageFont.truetype(font=font_2b_p, size=16, index=0)
font_2_17 = ImageFont.truetype(font=font_2_p, size=17, index=0)
font_2b_17 = ImageFont.truetype(font=font_2b_p, size=17, index=0)
font_2_18 = ImageFont.truetype(font=font_2_p, size=18, index=0)
font_2b_18 = ImageFont.truetype(font=font_2b_p, size=18, index=0)
font_2_19 = ImageFont.truetype(font=font_2_p, size=19, index=0)
font_2b_19 = ImageFont.truetype(font=font_2b_p, size=19, index=0)
font_2_20 = ImageFont.truetype(font=font_2_p, size=20, index=0)
font_2b_20 = ImageFont.truetype(font=font_2b_p, size=20, index=0)
font_2_22 = ImageFont.truetype(font=font_2_p, size=22, index=0)
font_2b_22 = ImageFont.truetype(font=font_2b_p, size=22, index=0)
font_2_24 = ImageFont.truetype(font=font_2_p, size=24, index=0)
font_2b_24 = ImageFont.truetype(font=font_2b_p, size=24, index=0)
font_2_26 = ImageFont.truetype(font=font_2_p, size=26, index=0)
font_2b_26 = ImageFont.truetype(font=font_2b_p, size=26, index=0)
font_2_28 = ImageFont.truetype(font=font_2_p, size=28, index=0)
font_2b_28 = ImageFont.truetype(font=font_2b_p, size=28, index=0)
font_2_32 = ImageFont.truetype(font=font_2_p, size=32, index=0)
font_2b_32 = ImageFont.truetype(font=font_2b_p, size=32, index=0)

_i_ = Image.new('RGBA', (0, 0))
_d_ = ImageDraw.Draw(_i_)


def render_skill(
        card_name,
        card_name_c,
        card_text,
        card_type,
):
    f_name = 'images/' + card_name.lower().replace(' ', '-').replace('\'', '').replace(':', '').replace(
        ',', '').replace('!', '') + '.png'
    img = Image.new('RGBA', (286, 395))
    d = ImageDraw.Draw(img)
    box_all = (0, 0, 286, 395)
    with Image.open(f_name) as _f:
        _crop = _f.crop(box_all)
        img.paste(_crop, box_all, _crop)
    if card_type and card_type != '无':
        with Image.open('render/skill_2.png') as _f:
            _crop = _f.crop(box_all)
            img.paste(_crop, box_all, _crop)
        d.text((142, 356), card_type, 'white', font=font_1_22, anchor='ma', align='center',
               stroke_width=2, stroke_fill='black')
        tag_tf = 1
    else:
        with Image.open('render/skill_1.png') as _f:
            _crop = _f.crop(box_all)
            img.paste(_crop, box_all, _crop)
        tag_tf = 0

    d.text((142, 222), card_name_c, 'white', font=font_1_26, anchor='ma', align='center',
           stroke_width=2, stroke_fill='black')

    out_lines = break_lines(card_text, tag_tf)
    font_paras = [[None,
                   (font_2_19, font_2b_19, 21, 300),
                   (font_2_19, font_2b_19, 21, 290),
                   (font_2_18, font_2b_18, 20, 280),
                   (font_2_17, font_2b_17, 19, 270),
                   (font_2_16, font_2b_16, 18, 260)],
                  [None,
                   (font_2_19, font_2b_19, 21, 295),
                   (font_2_19, font_2b_19, 21, 285),
                   (font_2_18, font_2b_18, 20, 275),
                   (font_2_17, font_2b_17, 19, 265),
                   (font_2_16, font_2b_16, 18, 255)]]
    f_para = font_paras[tag_tf][len(out_lines)]
    f_a = f_para[0]
    f_b = f_para[1]
    f_size = f_para[2]
    y = f_para[3]
    for line in out_lines:
        text_img_check = [z2(line[0][_i], f_size, f_b) if _i in line[1] else z2(line[0][_i], f_size, f_a)
                          for _i in range(len(line[0]))]
        ch_len = sum([x[1] for x in text_img_check])
        x = 142 - ch_len // 2
        for ch_img_check in text_img_check:
            img.paste(ch_img_check[0], (x, y), mask=ch_img_check[0])
            x += ch_img_check[1]
        y += int(f_size * 1.1)

    # img.show()
    img.save('skill/' + card_name.replace(':', '') + '.png')


def minion_x2yz(x: int):
    y = 305 - int(math.cos((x - 151) / 1000 * math.pi) * 140)
    z = math.sin((x - 151) / 1600 * math.pi) * 40
    print(x, y, z)
    return y, z


def render_item(
        card_name,
        card_name_c,
        card_text
):
    f_name = 'images/' + card_name.lower().replace(' ', '-').replace('\'', '').replace(':', '').replace(
        ',', '').replace('!', '') + '.png'
    img = Image.new('RGBA', (286, 395))
    d = ImageDraw.Draw(img)
    box_all = (0, 0, 286, 395)
    with Image.open(f_name) as _f:
        _crop = _f.crop(box_all)
        img.paste(_crop, box_all, _crop)

    with Image.open('render/item.png') as _f:
        _crop = _f.crop(box_all)
        img.paste(_crop, box_all, _crop)
    # 牌名
    name_img_check = [z1(ch, 30, font_1_28) for ch in card_name_c]
    ch_len = sum([x[1] for x in name_img_check])
    _dy = 0
    if ch_len > 250:
        name_img_check = [z1(ch, 23, font_1_21) for ch in card_name_c]
        ch_len = sum([x[1] for x in name_img_check])
        _dy = 20
    elif ch_len > 210:
        name_img_check = [z1(ch, 26, font_1_24) for ch in card_name_c]
        ch_len = sum([x[1] for x in name_img_check])
        _dy = 10
    print(ch_len)
    x = 155 - ch_len // 2
    for ch_img_check in name_img_check:
        y, z = minion_x2yz(x)
        img_rotated = ch_img_check[0].rotate(-z, resample=Image.BICUBIC)
        img.paste(img_rotated, (x - ch_img_check[1] // 2, y + 34), mask=img_rotated)
        x += ch_img_check[1]
    # d.text((142, 222), card_name_c, 'white', font=font_1_26, anchor='ma', align='center',
    #        stroke_width=2, stroke_fill='black')

    # 规则
    out_lines = break_lines(card_text, False)
    font_paras = [None,
                  (font_2_19, font_2b_19, 21, 300),
                  (font_2_19, font_2b_19, 21, 290),
                  (font_2_18, font_2b_18, 20, 280),
                  (font_2_17, font_2b_17, 19, 270),
                  (font_2_16, font_2b_16, 18, 260)]
    f_para = font_paras[len(out_lines)]
    f_a = f_para[0]
    f_b = f_para[1]
    f_size = f_para[2]
    y = f_para[3]
    for line in out_lines:
        text_img_check = [z3(line[0][_i], f_size, f_b) if _i in line[1] else z3(line[0][_i], f_size, f_a)
                          for _i in range(len(line[0]))]
        ch_len = sum([x[1] for x in text_img_check])
        x = 142 - ch_len // 2
        for ch_img_check in text_img_check:
            img.paste(ch_img_check[0], (x, y), mask=ch_img_check[0])
            x += ch_img_check[1]
        y += int(f_size * 1.1)

    # img.show()
    img.save('item/' + card_name.replace(':', '') + '.png')


def break_lines(text, t):
    if t:
        line_limit = [None,
                      [185, 185],
                      [185, 185, 185],
                      [190, 190, 190, 190],
                      [190, 190, 190, 190, 190],
                      [195, 195, 195, 195, 195, 195],
                      [195, 195, 195, 195, 195, 195, 195]]
    else:
        line_limit = [None,
                      [185, 185],
                      [185, 185, 185],
                      [190, 190, 190, 190],
                      [190, 190, 190, 190, 190],
                      [195, 195, 195, 195, 195, 195],
                      [195, 195, 195, 195, 195, 195, 195]]
    raw_lines = text.split('\n')
    detailed_lines = []
    for line in raw_lines:
        bold = []
        line = line.replace('<i>', '').replace('</i>', '').replace('$', '').replace('#', '')
        while '<b>' in line or '</b>' in line:
            start = max(line.find('<b>'), 0)
            line = line.replace('<b>', '', 1)
            end = line.find('</b>')
            if end == -1:
                end = len(line)
            bold += range(start, end)
            line = line.replace('</b>', '', 1)
        detailed_lines.append((line, bold))
    print(detailed_lines)
    line_result = 0
    line_all = len(detailed_lines)
    f_try = font_2_18
    x_lists = [[_d_.textsize(c, f_try)[0] for c in detailed_lines[ll][0]] for ll in range(line_all)]
    print(x_lists)
    if line_all == 1:
        x_list = x_lists[0]
        if sum(x_list) < 190:
            line_result = 1
    if line_result == 0 and len(detailed_lines) < 3:
        if sum([int(math.ceil(sum(x_lists[ll]) / 190)) for ll in range(line_all)]) < 3:
            line_result = 2
    if line_result == 0 and len(detailed_lines) < 4:
        if sum([int(math.ceil(sum(x_lists[ll]) / 205)) for ll in range(line_all)]) < 4:
            line_result = 3
    if line_result == 0 and len(detailed_lines) < 5:
        if sum([int(math.ceil(sum(x_lists[ll]) / 205)) for ll in range(line_all)]) < 5:
            line_result = 4
    if line_result == 0 and len(detailed_lines) < 6:
        if sum([int(math.ceil(sum(x_lists[ll]) / 205)) for ll in range(line_all)]) < 6:
            line_result = 5
    print(line_result)
    output = []
    line_now = 0
    for ii in range(line_all):
        input_line = ['', []]
        limit_now = line_limit[line_result][line_now]
        input_x = 0
        this_detailed_line = detailed_lines[ii]
        this_x_list = x_lists[ii]
        for jj in range(len(this_detailed_line[0])):
            if input_x + this_x_list[jj] > limit_now:
                if this_detailed_line[0][jj] in '0123456789+/，：；。！）':
                    _start = jj
                    _continue_flag = True
                    while _continue_flag and this_detailed_line[0][_start] in '0123456789+/，：；。！）':
                        _start -= 1
                        input_x -= this_x_list[_start]
                        input_line[0] = input_line[0][:-1]
                        if _start in this_detailed_line[1]:
                            input_line[1].pop(_start)
                        if this_detailed_line[0][_start - 1] not in '0123456789+/，：；。！）' and this_detailed_line[0][
                            _start] not in '，：；。！）':
                            _continue_flag = False
                        if this_detailed_line[0][_start - 1] in '(（' and this_detailed_line[0][_start] in '0123456789':
                            _continue_flag = True
                    # 强行换行
                    line_now += 1
                    limit_now = line_limit[line_result][line_now]
                    input_x = sum(this_x_list[_start:jj + 1])
                    output.append(input_line)
                    input_line = [this_detailed_line[0][_start:jj + 1], []]
                    for __x in range(_start, jj + 1):
                        if __x in this_detailed_line[1]:
                            input_line[1].append(__x - _start)

                else:
                    line_now += 1
                    limit_now = line_limit[line_result][line_now]
                    input_x = this_x_list[jj]
                    output.append(input_line)
                    input_line = [this_detailed_line[0][jj], []]
                    if jj in this_detailed_line[1]:
                        input_line[1].append(0)
            else:
                input_x += this_x_list[jj]
                input_line[0] += this_detailed_line[0][jj]
                if jj in this_detailed_line[1]:
                    input_line[1].append(len(input_line[0]) - 1)
        line_now += 1
        output.append(input_line)

    print(output)
    print()
    return output


def z1(c='爱', s=28, f=font_1_26):
    _check = c.isascii()
    tx = _d_.textsize(c, f)
    if _check:
        w = tx[0] + 4
    else:
        w = s
    img = Image.new('RGBA', (w, s))
    d = ImageDraw.Draw(img)
    d.text((w // 2, s // 2), c, font=f, anchor='mm', fill='white', stroke_width=3, stroke_fill='black')
    # d.polygon([(0, 0), (0, s), (w, s), (w, 0)], outline='black')
    return img, w


def z2(c='爱', s=28, f=font_2_26):
    _check = c.isascii()
    tx = _d_.textsize(c, f)
    if _check:
        w = tx[0]
    else:
        w = s
    img = Image.new('RGBA', (w, s))
    d = ImageDraw.Draw(img)
    d.text((w // 2, s // 2), c, anchor='mm', font=f, fill='black')
    # d.text((w // 2, - int(round(s / 11))), c, anchor='ma', font=f, fill='black')
    # d.polygon([(0, 0), (0, s-1), (w-1, s-1), (w-1, 0)], outline='black')
    return img, w - 1


def z3(c='爱', s=28, f=font_2_26):
    _check = c.isascii()
    tx = _d_.textsize(c, f)
    if _check:
        w = tx[0]
    else:
        w = s
    img = Image.new('RGBA', (w, s))
    d = ImageDraw.Draw(img)
    d.text((w // 2, s // 2), c, anchor='mm', font=f, fill='white')
    # d.text((w // 2, - int(round(s / 11))), c, anchor='ma', font=f, fill='black')
    # d.polygon([(0, 0), (0, s-1), (w-1, s-1), (w-1, 0)], outline='black')
    return img, w - 1


def main():
    for _x_ in d_skill[0]:
        _skill_d = SKILL_D[SKILL[_x_]]
        _skill_type = _skill_d[0]
        for _y_ in range(1, 6):
            render_skill(_x_ + ' ' + str(_y_), SKILL_L[SKILL[_x_]] + str(_y_), _skill_d[_y_][1], S_TYPE_L[_skill_type])

    for _x_ in d_item[0]:
        _item_d = ITEM_D[ITEM[_x_]]
        for _y_ in range(_item_d[0], 5):
            render_item(_x_ + ' ' + str(_y_), ITEM_L[ITEM[_x_]] + str(_y_), _item_d[_y_])


if __name__ == "__main__":
    main()
