import requests
import json
import re
import pprint
from pyecharts.charts import Map, Geo
from pyecharts import options as opts

if __name__ == '__main__':
    result = requests.get(
        'https://interface.sina.cn/news/wap/fymap2020_data.d.json?1580097300739&&callback=sinajp_1580097300873005379567841634181')
    json_str = re.search("\(+([^)]*)\)+", result.text).group(1)

    html = f"{json_str}"
    table = json.loads(f"{html}")
    pp = pprint.PrettyPrinter(indent=4)
    data = []
    for province in table['data']['list']:
        pp.pprint(province)
        data.append((province['name'], province['value']))

        for city in province['city']:
            data.append((city['name'], city['conNum']))
            pp.pprint(city)
map_p = Map()
map_p.set_global_opts(title_opts=opts.TitleOpts(title="实时疫情图"), visualmap_opts=opts.VisualMapOpts(max_=100))
map_p.add("确诊", data, maptype="china")
map_p.render("ncov.html")  # 生成html文件
