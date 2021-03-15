from pyecharts import options as opts
from pyecharts.charts import Boxplot,Grid,Bar,Line
from pyecharts import globals
from pyecharts.globals import ThemeType
import operator
import json
from pyecharts.commons.utils import JsCode
import numpy as np
def find_proportion_render(x,y,z,part_name,main_name,query,table_path,answer):
    x=list(map(str,x))
    y=list(map(float,y))
    z=list(map(float,z))
    colorList = ['#f36c6c', '#e6cf4e', '#20d180', '#0093ff']
    y_part=[]
    y_main=[]
    for i in range(len(y)):
        percentage=y[i]/z[i]*100
        percentage=str(percentage).split('.')[0] + '.' + str(percentage).split('.')[1][:2]
        y_part.append(
            opts.BarItem(
                name=x[i],
                value=y[i],
                label_opts=opts.LabelOpts(position="insideTop",formatter=str(percentage)+"%"),
                itemstyle_opts=opts.ItemStyleOpts(color=colorList[2])
            )
        )
        y_main.append(
            opts.BarItem(
                name=x[i],
                value=z[i]-y[i],
            )
        )
    bar = Bar()
    bar.add_xaxis(x)
    bar.add_yaxis('', y_axis=y_part, stack='stack1', label_opts=opts.LabelOpts(position="insideTop"),itemstyle_opts=opts.ItemStyleOpts(color=colorList[2]),tooltip_opts=opts.TooltipOpts(formatter=part_name+':{c}')),
    bar.add_yaxis('', y_axis=y_main, stack='stack1',label_opts=opts.LabelOpts(is_show=False),color="gray",tooltip_opts=opts.TooltipOpts(formatter=main_name+':{c}'))
    bar.set_global_opts(
        datazoom_opts=[opts.DataZoomOpts(range_start=10, range_end=90),
                       opts.DataZoomOpts(type_="inside")],
        legend_opts=opts.LegendOpts(is_show=False),
        graphic_opts=[opts.GraphicText(
            graphic_item=opts.GraphicItem(
                left="center",
                top="bottom",

            ),
            graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                # 可以通过jsCode添加js代码，也可以直接用字符串
                text=['\n' + "Q:" + ' ' + query + '\n' + 'A:' + ' ' + answer],
                font="14px Microsoft YaHei",
                graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                    fill="#333"
                )
            )
        )]
    )
    bar.render("aggregation.html")
    grid = Grid(init_opts=opts.InitOpts(
        width="100%",
        height="100%",
        renderer=globals.RenderType.SVG, ))
    grid.add(bar, grid_opts={'left': '20%', 'bottom': '34%'})
    option1 = grid.dump_options_with_quotes()
    option1 = json.loads(option1)
    option = {"option": [option1], "query": query}
    return option
