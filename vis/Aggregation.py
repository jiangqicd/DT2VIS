from pyecharts import options as opts
from pyecharts.charts import Boxplot,Grid,Bar,Line
from pyecharts import globals
from pyecharts.globals import ThemeType
import operator
import json
from pyecharts.commons.utils import JsCode
import numpy as np
def find_aggregation_render(x,y,flag,query,table_path,answer,y_name):
    colorList = ['#f36c6c', '#e6cf4e', '#20d180', '#0093ff']
    x_sum=["Sum"]
    Sum=[]
    Sum.append(sum(y))
    mean=np.mean(y)
    y1=[]
    y2=[]
    for i in range(len(y)):
        if y[i]>=mean:
            y1.append(round(mean,2))
            y2.append(
                opts.BarItem(
                    name=x[i],
                    value=round(y[i]-mean,2),
                    label_opts=opts.LabelOpts(formatter="+{c}"),
                    itemstyle_opts=opts.ItemStyleOpts(color="red")
                )
            )
        else:
            y1.append(round(y[i],2))
            y2.append(
                opts.BarItem(
                    name=x[i],
                    value=round(mean-y[i], 2),
                    label_opts=opts.LabelOpts(formatter="-{c}"),
                    itemstyle_opts=opts.ItemStyleOpts(color="green",opacity=0.3)
                )
            )
    if flag=="mean":
        bar = Bar()
        bar.add_xaxis(x)
        bar.add_yaxis('', y_axis=y1, stack='stack1', label_opts=opts.LabelOpts(is_show=False), color="white",
                      markline_opts=opts.MarkLineOpts(
                          data=[opts.MarkLineItem(name="mean:", y=round(mean, 2))],
                          label_opts=opts.LabelOpts(
                              formatter="Mean:{c}",
                              color="black"
                          ),
                          linestyle_opts=opts.LineStyleOpts(color="gray")
                      ),
                      )
        bar.add_yaxis('', y_axis=y2, stack='stack1')
        bar.set_global_opts(
        datazoom_opts=[opts.DataZoomOpts(range_start=10,range_end=90), opts.DataZoomOpts(type_="inside")],
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=40,font_size='100%'),name_textstyle_opts=opts.TextStyleOpts(font_size="100%")),
        yaxis_opts=opts.AxisOpts(min_=int(min(y)-(max(y)-min(y))/10),name=y_name,axislabel_opts=opts.LabelOpts(font_size="100%"),name_textstyle_opts=opts.TextStyleOpts(font_size="100%")),
            graphic_opts=[opts.GraphicText(
                graphic_item=opts.GraphicItem(
                    left="center",
                    top="bottom",

                ),
                graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                    # 可以通过jsCode添加js代码，也可以直接用字符串
                    text=['\n' + "Q:" + ' ' + query + '\n'+"\n" + 'A:' + ' ' + answer],
                    font="14px Microsoft YaHei",
                    graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                        fill="#333"
                    )
                )
            )]
        )
        bar.render("aggregation.html")
        grid = Grid( init_opts=opts.InitOpts(
            width="100%",
            height="100%",
            renderer= globals.RenderType.SVG,))
        grid.add(bar,  grid_opts={'left':'15%','bottom':'34%'})
        grid1=Grid()
        grid1.add(bar,  grid_opts={'left':'15%','bottom':'34%'})
        grid1.render("mean.html")
        option1=grid.dump_options_with_quotes()
        option1=json.loads(option1)
        option={"option":[option1],"query":query}
        return option
    elif flag=="sum":
        bar = Bar()
        bar.add_xaxis(x_sum)
        bar.add_yaxis('',Sum,label_opts=opts.LabelOpts(position="inside",formatter="Sum:{c}"),color=colorList[0])
        for i in range(len(y)):
            Y=[]
            Y.append(y[i])
            r=str(x[i])
            bar.add_yaxis('',Y, stack='stack1', label_opts=opts.LabelOpts(position="inside",formatter=r+":{c}"),tooltip_opts=opts.TooltipOpts(is_show=False))
        bar.set_global_opts(
            datazoom_opts=[opts.DataZoomOpts(range_start=10,range_end=90,orient="vertical"), opts.DataZoomOpts(type_="inside")],
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
        grid = Grid( init_opts=opts.InitOpts(
            width="100%",
            height="100%",
            renderer= globals.RenderType.SVG,))
        grid.add(bar,  grid_opts={'left':'15%','bottom':'34%'})
        option1=grid.dump_options_with_quotes()
        option1=json.loads(option1)
        option={"option":[option1],"query":query}
        return option