# -*- coding: utf-8 -*-

__author__ = "gao"

# from pyecharts import Bar,configure, Line
# configure(output_image="jpeg")
# bar = Line("我的第一个图表", "这里是副标题")
# bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90], mark_point_symbolsize=0,tooltip_tragger="axis",is_label_emphasis=True)
# bar.add("服装0", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [7, 2, 35, 17, 25, 60], label_emphasis_pos="bottom", is_legend_show=True,symbol_size=0, line_opacity=0,tooltip_tragger="axis")
# bar.print_echarts_options() # 该行只为了打印配置项，方便调试时使用
# bar.render()    # 生成本地 HTML 文件

from pyecharts import Bar, Timeline
from random import randint
attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
bar_1 = Bar("2012 年销量", "数据纯属虚构")
bar_1.add("春季", attr, [randint(10, 100) for _ in range(6)])
bar_1.add("夏季", attr, [randint(10, 100) for _ in range(6)])
bar_1.add("秋季", attr, [randint(10, 100) for _ in range(6)])
bar_1.add("冬季", attr, [randint(10, 100) for _ in range(6)])

bar_2 = Bar("2013 年销量", "数据纯属虚构")
bar_2.add("春季", attr, [randint(10, 100) for _ in range(6)])
bar_2.add("夏季", attr, [randint(10, 100) for _ in range(6)])
bar_2.add("秋季", attr, [randint(10, 100) for _ in range(6)])
bar_2.add("冬季", attr, [randint(10, 100) for _ in range(6)])

bar_3 = Bar("2014 年销量", "数据纯属虚构")
bar_3.add("春季", attr, [randint(10, 100) for _ in range(6)])
bar_3.add("夏季", attr, [randint(10, 100) for _ in range(6)])
bar_3.add("秋季", attr, [randint(10, 100) for _ in range(6)])
bar_3.add("冬季", attr, [randint(10, 100) for _ in range(6)])

bar_4 = Bar("2015 年销量", "数据纯属虚构")
bar_4.add("春季", attr, [randint(10, 100) for _ in range(6)])
bar_4.add("夏季", attr, [randint(10, 100) for _ in range(6)])
bar_4.add("秋季", attr, [randint(10, 100) for _ in range(6)])
bar_4.add("冬季", attr, [randint(10, 100) for _ in range(6)])

bar_5 = Bar("2016 年销量", "数据纯属虚构")
bar_5.add("春季", attr, [randint(10, 100) for _ in range(6)])
bar_5.add("夏季", attr, [randint(10, 100) for _ in range(6)])
bar_5.add("秋季", attr, [randint(10, 100) for _ in range(6)])
bar_5.add("冬季", attr, [randint(10, 100) for _ in range(6)], is_legend_show=True)

timeline = Timeline(is_auto_play=True, timeline_bottom=0)
timeline.add(bar_1, '2012 年')
timeline.add(bar_2, '2013 年')
timeline.add(bar_3, '2014 年')
timeline.add(bar_4, '2015 年')
timeline.add(bar_5, '2016 年')
timeline.render()



