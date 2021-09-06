from json import loads, dumps
import pandas

pandas.read_excel(r'D:\Desktop\佣兵统计.xlsx').to_json(r'D:\Desktop\佣兵统计.json')
with open(r'D:\Desktop\佣兵统计.json', 'r', encoding='utf-8') as f:
    d = loads(f.read())
o = [tuple(d['ename'].values()), tuple(d['cname'].values()), tuple(d['类'].values()), tuple(d['race'].values()),
     tuple(d['i1'].values()), tuple(d['i2'].values()), tuple(d['i3'].values()), tuple(d['s1'].values()),
     tuple(d['s2'].values()), tuple(d['s3'].values()), tuple(d['a30'].values())]
with open('data.json', 'w', encoding='utf-8') as f:
    print(dumps(o, separators=(',', ':')), file=f)
