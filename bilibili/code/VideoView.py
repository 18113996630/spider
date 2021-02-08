from pyecharts.charts import Bar
from pyecharts import options as opts
import pandas as pd

pd.set_option('display.max_columns', None)

data = pd.read_csv('up.csv').sort_values('粉丝数量', ascending=False).head(5)
bar = (
    Bar()
        .add_xaxis(data['昵称'].tolist())
        .add_yaxis('粉丝数量', data['粉丝数量'].tolist())
        .add_yaxis('点赞量', data['点赞量'].tolist())
        .add_yaxis('视频播放量', data['视频播放量'].tolist())
        .set_global_opts(title_opts=opts.TitleOpts(title="个人信息"))
)
bar.render()