from json import loads, dumps
import pandas

pandas.read_excel(r'佣兵统计.xlsx').to_json(r'佣兵统计.json')
with open(r'佣兵统计.json', 'r', encoding='utf-8') as f:
    d = loads(f.read())
o = [tuple(d['name'].values()), tuple(d['name_c'].values()), tuple(d['class'].values()), tuple(d['race'].values()),
     tuple(d['i1'].values()), tuple(d['i2'].values()), tuple(d['i3'].values()), tuple(d['i4'].values()),
     tuple(d['s1'].values()), tuple(d['s2'].values()), tuple(d['s3'].values()), tuple(d['s4'].values())
     ] + [tuple(d['a' + str(i)].values()) for i in range(1, 31)]
with open('data_merc.json', 'w', encoding='utf-8') as f:
    print(dumps(o, separators=(',', ':')), file=f)

pandas.read_excel(r'技能统计.xlsx').to_json(r'技能统计.json')
with open(r'技能统计.json', 'r', encoding='utf-8') as f:
    d = loads(f.read())
o = [tuple(d['name'].values()), tuple(d['name_c'].values()), tuple(d['school'].values()),
     tuple(d['a1'].values()), tuple(d['a2'].values()), tuple(d['a3'].values()),
     tuple(d['a4'].values()), tuple(d['a4'].values()),
     tuple(d['c1'].values()), tuple(d['c2'].values()), tuple(d['c3'].values()),
     tuple(d['c4'].values()), tuple(d['c5'].values())]
with open('data_skill.json', 'w', encoding='utf-8') as f:
    print(dumps(o, separators=(',', ':')), file=f)

pandas.read_excel(r'装备统计.xlsx').to_json(r'装备统计.json')
with open(r'装备统计.json', 'r', encoding='utf-8') as f:
    d = loads(f.read())
o = [tuple(d['name'].values()), tuple(d['name_c'].values()),
     tuple(d['c1'].values()), tuple(d['c2'].values()), tuple(d['c3'].values()), tuple(d['c4'].values())]
with open('data_item.json', 'w', encoding='utf-8') as f:
    print(dumps(o, separators=(',', ':')), file=f)
