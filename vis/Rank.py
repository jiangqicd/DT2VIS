from pyecharts import options as opts
from pyecharts.charts import Boxplot,Grid,Bar
from pyecharts import globals
from pyecharts.globals import ThemeType
import operator
import json
from pyecharts.commons.utils import JsCode
def find_rank_render(x,y,query,table_path,answer):
    colorList = ['#f36c6c', '#e6cf4e', '#20d180', '#0093ff'];
    for i in range(len(y)):
        for j in range(0,len(y)-i-1):
            if y[j]>y[j+1]:
                y[j],y[j+1]=y[j+1],y[j]
                x[j],x[j+1]=x[j+1],x[j]
    Y=[]
    for i in range(len(y)):
        if i>len(y)-4:
            Y.append(
                opts.BarItem(
                    name=x[i],
                    value=y[i],
                    label_opts=opts.LabelOpts(position='right'),
                    itemstyle_opts=opts.ItemStyleOpts(color=colorList[len(y)-1-i])
                )
            )
        else:
            Y.append(
                opts.BarItem(
                    name=x[i],
                    value=y[i],
                    label_opts=opts.LabelOpts(position='right'),
                    itemstyle_opts=opts.ItemStyleOpts(color=colorList[3])
                )
            )
    bar=Bar()
    bar.add_xaxis(x)
    bar.add_yaxis('',y_axis=Y)
    bar.reversal_axis()
    bar.set_global_opts(
        xaxis_opts=opts.AxisOpts(is_show=False),
        yaxis_opts=opts.AxisOpts(
            type_='category',
            interval=True,
            axisline_opts=opts.AxisLineOpts(is_show=False),
            axistick_opts=opts.AxisTickOpts(is_show=False),
            axispointer_opts=opts.AxisPointerOpts(label=opts.LabelOpts(is_show=True,margin=30)),
            axislabel_opts=opts.LabelOpts(
                rotate=10
            )
        ),
        graphic_opts=[opts.GraphicText(
            graphic_item=opts.GraphicItem(
                left="center",
                top="bottom",
                z=100,
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
    grid.add(bar,  grid_opts={'left':'20%','bottom':'34%'})
    option1=grid.dump_options_with_quotes()
    option1=json.loads(option1)
    option={"option":[option1],"query":query}
    return option
    # Max=0
    # y=[]
    # data=[]
    # label=[]
    # boxplot = Boxplot()
    # boxplot.add_xaxis(xaxis_data=label)
    # for i in range(len(Y)):
    #     print(Y[i][0])
    #     data.append(Y[i][1])
    #     label.append(Y[i][0])
    #     # boxplot.add_yaxis(series_name=Y[i][0],y_axis=boxplot.prepare_data(data))
    #     for j in Y[i][1]:
    #         y.append(j)
    # boxplot.add_yaxis(series_name="", y_axis=boxplot.prepare_data(data))
    # boxplot.set_global_opts(
    #     yaxis_opts=opts.AxisOpts(name="Distribution",axislabel_opts=opts.LabelOpts(font_size="100%"),name_textstyle_opts=opts.TextStyleOpts(font_size="100%")),
    #     legend_opts=opts.LegendOpts(is_show=False),
    #     xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=40,interval=0,font_size='100%'),name="Category",name_textstyle_opts=opts.TextStyleOpts(font_size="100%")),
    # )
    #
    # bar=Bar({"theme": ThemeType.MACARONS})
    # bar.add_xaxis(xaxis_data=x)
    # for i in range(len(Y)):
    #     max_index, max_number = max(enumerate(Y[i][1]), key=operator.itemgetter(1))
    #     min_index, min_number = min(enumerate(Y[i][1]), key=operator.itemgetter(1))
    #     if max_number>Max:
    #         Max=max_number
    #     bar.add_yaxis(Y[i][0],y_axis=Y[i][1],markpoint_opts=opts.MarkPointOpts(
    #         data=[opts.MarkPointItem(coord=[max_index,max_number*1.01],value="MAX",name="最大值",itemstyle_opts=opts.ItemStyleOpts(opacity=0.6)),opts.MarkPointItem(coord=[min_index,min_number*1.05],value="MIN",name="最小值",itemstyle_opts=opts.ItemStyleOpts(opacity=0.6))]
    #     ),
    #                   markline_opts=opts.MarkLineOpts(
    #                       data=[opts.MarkLineItem(type_="average",name="平均值")]
    #                   ))
    # bar.set_global_opts(
    #     yaxis_opts=opts.AxisOpts(max_=Max*1.2,name="Distribution", axislabel_opts=opts.LabelOpts(font_size="100%"),
    #                              name_textstyle_opts=opts.TextStyleOpts(font_size="100%")),
    #     xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=40, interval=0, font_size='100%'),
    #                              name=x_name, name_textstyle_opts=opts.TextStyleOpts(font_size="100%")),
    # )
    # grid = Grid( init_opts=opts.InitOpts(
    #     width="100%",
    #     height="100%",
    #     renderer= globals.RenderType.SVG,))
    # grid.add(boxplot,  grid_opts={'left':'20%','bottom':'34%'})
    # grid1 = Grid( init_opts=opts.InitOpts(
    #     width="100%",
    #     height="100%",
    #     renderer= globals.RenderType.SVG,))
    # grid1.add(bar,grid_opts={'left':'20%','bottom':'34%'})
    # option1=grid.dump_options_with_quotes()
    # option1=json.loads(option1)
    # option2=grid1.dump_options_with_quotes()
    # option2=json.loads(option2)
    # option={"option":[option1,option2],"query":query}
    # return option