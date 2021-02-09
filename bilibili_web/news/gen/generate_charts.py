import datetime
import os
import time

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import WordCloud


def yesterday():
    today = datetime.datetime.today()
    one = datetime.timedelta(days=1)
    yesterday = today - one
    return yesterday.strftime('%Y%m%d')

def gen(file_name: str):
    real_name = file_name + '_' + datetime.datetime.now().strftime('%Y%m%d') + '.html'
    if os.path.exists(real_name):
        return
    else:
        print('开始生成')
        data = pd.read_csv(r'D:\python-workspace\bilibili_web\news\gen\video.csv', encoding='GBK').head(20)
        cnt = {}
        for i in data['tags']:
            for word in i.split('|'):
                cnt[word] = cnt.get(word, 0) + 1
        res = zip(cnt.keys(), cnt.values())
        d = []
        for r in res:
            d.append(r)
        (
            WordCloud()
                .add('danmu', d, word_size_range=[10, 25], width='350', height='350', pos_left='-50', pos_top='-100')
                .set_global_opts(
                title_opts=opts.TitleOpts(
                    title_textstyle_opts=opts.TextStyleOpts(font_size=23)
                ),
                tooltip_opts=opts.TooltipOpts(is_show=False),
            )
                .render(r"D:\python-workspace\bilibili_web\news\templates\{file}".format(file=real_name))
        )


if __name__ == '__main__':
    print(yesterday())
