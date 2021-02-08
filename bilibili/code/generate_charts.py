import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import WordCloud

if __name__ == '__main__':
    data = pd.read_csv('video.csv')
    tags = []
    cnt = {}
    for i in data['标签']:
        for word in i.split('|'):
            cnt[word] = cnt.get(word, 0) + 1
    res = zip(cnt.keys(), cnt.values())
    d = []
    for r in res:
        d.append(r)
    (
        WordCloud()
            .add('danmu', d, word_size_range=[20, 66], shape='triangle-forward')
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="热点分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
            .render("xiaojiayu.html")
    )
