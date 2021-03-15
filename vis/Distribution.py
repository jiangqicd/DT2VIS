from pyecharts import options as opts
from pyecharts.charts import Boxplot,Grid,Bar
from pyecharts import globals
from pyecharts.globals import ThemeType
import operator
import json
def find_distribution_render(x,Y,x_name,query,table_path,answer):
    Max=0
    y=[]
    data=[]
    label=[]
    boxplot = Boxplot()
    boxplot.add_xaxis(xaxis_data=label)
    for i in range(len(Y)):
        data.append(Y[i][1])
        label.append(Y[i][0])
        # boxplot.add_yaxis(series_name=Y[i][0],y_axis=boxplot.prepare_data(data))
        for j in Y[i][1]:
            y.append(j)
    boxplot.add_yaxis(series_name="", y_axis=boxplot.prepare_data(data))
    boxplot.set_global_opts(
        yaxis_opts=opts.AxisOpts(name="Distribution",axislabel_opts=opts.LabelOpts(font_size="100%"),name_textstyle_opts=opts.TextStyleOpts(font_size="100%")),
        legend_opts=opts.LegendOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=40,interval=0,font_size='100%'),name="Category",name_textstyle_opts=opts.TextStyleOpts(font_size="100%")),
        graphic_opts=[opts.GraphicText(
            graphic_item=opts.GraphicItem(
                left="center",
                top="bottom",
                z=100,
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

    bar=Bar({"theme": ThemeType.MACARONS})
    bar.add_xaxis(xaxis_data=x)
    for i in range(len(Y)):
        max_index, max_number = max(enumerate(Y[i][1]), key=operator.itemgetter(1))
        min_index, min_number = min(enumerate(Y[i][1]), key=operator.itemgetter(1))
        if max_number>Max:
            Max=max_number
        bar.add_yaxis(Y[i][0],label_opts=opts.LabelOpts(is_show=False),y_axis=Y[i][1],markpoint_opts=opts.MarkPointOpts(
            data=[opts.MarkPointItem(coord=[max_index,max_number*1.01],value="MAX",name="最大值",itemstyle_opts=opts.ItemStyleOpts(opacity=0.6)),opts.MarkPointItem(coord=[min_index,min_number*1.05],value="MIN",name="最小值",itemstyle_opts=opts.ItemStyleOpts(opacity=0.6))]
        ),
                      markline_opts=opts.MarkLineOpts(
                          data=[opts.MarkLineItem(type_="average",name="平均值")]
                      ))
    bar.set_global_opts(
        datazoom_opts=[opts.DataZoomOpts(range_start=10, range_end=90),
                       opts.DataZoomOpts(type_="inside")],
        yaxis_opts=opts.AxisOpts( axislabel_opts=opts.LabelOpts(font_size="100%"),
                                 name_textstyle_opts=opts.TextStyleOpts(font_size="100%")),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=40, interval=0, font_size='100%'),
                                 name=x_name, name_textstyle_opts=opts.TextStyleOpts(font_size="100%")),
        graphic_opts=[opts.GraphicText(
            graphic_item=opts.GraphicItem(
                left="center",
                top="bottom",

            ),
            graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                # 可以通过jsCode添加js代码，也可以直接用字符串
                text=['\n' + "Q:" + ' ' + query + '\n' + "\n"+'A:' + ' ' + answer],
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
    grid.add(boxplot,  grid_opts={'left':'20%','bottom':'34%'})
    grid1 = Grid( init_opts=opts.InitOpts(
        width="100%",
        height="100%",
        renderer= globals.RenderType.SVG,))
    grid1.add(bar,grid_opts={'left':'20%','bottom':'34%'})
    option1=grid.dump_options_with_quotes()
    option1=json.loads(option1)
    option2=grid1.dump_options_with_quotes()
    option2=json.loads(option2)
    option={"option":[option1,option2],"query":query}
    return option