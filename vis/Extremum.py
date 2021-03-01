import pyecharts.options as opts
import json
from pyecharts import globals
from pyecharts.charts import Line,Grid
#Extremum_1
#For visualization X+Y+F e.g. Which year has the lowest gdp after 2015?
#X+Y e.g. Which year has the lowest gdp?

def find_extremum_render(x,y,x_name,y_name,query,operator,answer):
    x=list(map(str,x))
    y=list(map(float,y))
    makepoint=[]
    makeline=[]
    if operator=="MAX":
        makepoint.append(opts.MarkPointItem(type_="max",value="max",itemstyle_opts=opts.ItemStyleOpts(opacity=0.6)))
        makeline.append(opts.MarkPointItem(type_="max", value="max"))
    else:
        makepoint.append(opts.MarkPointItem(type_="min", value="min", itemstyle_opts=opts.ItemStyleOpts(opacity=0.6)))
        makeline.append(opts.MarkPointItem(type_="min", value="min"))
    line=Line()
    line.add_xaxis(x)
    line.add_yaxis(
        y_name,
        y_axis=y,
        symbol_size='100%',
        markpoint_opts=opts.MarkPointOpts(
            data=makepoint,
            symbol_size=50,
            label_opts=opts.LabelOpts(formatter=operator)
        ),
        markline_opts=opts.MarkLineOpts(
            data=makeline,
            label_opts=opts.LabelOpts(formatter=operator+":{c}")
        )
    )

    line.set_global_opts(
        yaxis_opts=opts.AxisOpts(min_=int(min(y)-(max(y)-min(y))/10),name=y_name,axislabel_opts=opts.LabelOpts(font_size="100%"),name_textstyle_opts=opts.TextStyleOpts(font_size="100%")),
        legend_opts=opts.LegendOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=40,font_size='100%'),name=x_name,name_textstyle_opts=opts.TextStyleOpts(font_size="100%")),
        graphic_opts=[opts.GraphicText(
            graphic_item=opts.GraphicItem(
                left="center",
                top="bottom",
                z=100,
            ),
            graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                # 可以通过jsCode添加js代码，也可以直接用字符串
                text=['\n' + "Q:" + ' ' + query + '\n' +"\n"+ 'A:' + ' ' + answer],
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
                            renderer= globals.RenderType.SVG,
                            ))
    grid.add(line,  grid_opts={'left':'20%','bottom':'34%'})
    # grid1=Grid()
    # grid1.add(line,  grid_opts={'left':'20%','bottom':'34%'})
    # grid1.render("MAX.html")
    option1=grid.dump_options_with_quotes()
    option1=json.loads(option1)
    option={"option":[option1],"query":query}
    return option