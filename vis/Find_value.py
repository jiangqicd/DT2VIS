from pyecharts import options as opts
from pyecharts.charts import Boxplot,Grid,Bar,Line,  Parallel
from pyecharts import globals
from pyecharts.globals import ThemeType
import operator
import json
from pyecharts.commons.utils import JsCode
import numpy as np
def find_value_render(query_filter,x_label,x,result,Data,query,table_path,answer):

    colorList = ['#f36c6c', '#e6cf4e', '#20d180', '#0093ff']
    # x = ['GDP', 'Industry', 'Architecture', 'Service']
    # y = [990865, 317109, 70904, 534233]
    # x1 = ["周一"]
    # y1 = [11]

    Y=[]
    # for i in range(len(y)):
    #     if i==0:
    #         Y.append(
    #             opts.BarItem(
    #                 name=x[i],
    #                 value=round(y[i], 2),
    #                 label_opts=opts.LabelOpts(position="insideTop"),
    #                 itemstyle_opts={
    #                     "normal": {
    #                         "color": colorList[0],
    #                         "barBorderRadius": [30, 30, 30, 30],
    #                     }
    #                 }
    #         ))
    #     else:
    #         Y.append(
    #             opts.BarItem(
    #                 name=x[i],
    #                 value=round(y[i], 2),
    #                 label_opts=opts.LabelOpts(position="insideTop"),
    #                 itemstyle_opts={
    #                     "normal": {
    #                         "color": "blue",
    #                         "barBorderRadius": [30, 30, 30, 30],
    #                     }
    #                 }
    #             ))
    bar1 = Bar()
    bar1.add_xaxis(x)
    bar1.add_yaxis(result[0][0], y_axis=result[0][1], label_opts=opts.LabelOpts(position="insideTop")
                  )
    bar1.set_global_opts(
        yaxis_opts=opts.AxisOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(
            axisline_opts=opts.AxisLineOpts(is_show=False),
            axispointer_opts=opts.AxisPointerOpts(is_show=False),
            axistick_opts=opts.AxisTickOpts(is_show=False)
        ),
        title_opts=opts.TitleOpts(
            subtitle="When the search condition is "+query_filter,
            pos_left='center'
        ),
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
    bar2 = Bar()
    bar2.add_xaxis(x)
    for i in range(len(result)):
       bar2.add_yaxis(result[i][0], y_axis=result[i][1]
                  )
    bar2.set_global_opts(
        yaxis_opts=opts.AxisOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(
            axisline_opts=opts.AxisLineOpts(is_show=False),
            axispointer_opts=opts.AxisPointerOpts(is_show=False),
            axistick_opts=opts.AxisTickOpts(is_show=False)
        ),
        title_opts=opts.TitleOpts(
            subtitle="\n"+"When the search condition is "+query_filter,
            pos_left='center'
        ),
        graphic_opts=[opts.GraphicText(
            graphic_item=opts.GraphicItem(
                left="center",
                top="bottom",
                z=100,
            ),
            graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                # 可以通过jsCode添加js代码，也可以直接用字符串
                text=['\n'+"\n" + "Q:" + ' ' + query + '\n' +"\n"+ 'A:' + ' ' + answer],
                font="16px Microsoft YaHei",
                graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                    fill="#333"
                )
            )
        )]
    )

    Label=[]
    data=[]
    for i in range(len(Data)):
        Label.append(str(Data[i][0]))
        data.append(Data[i][1])
    data=list(map(list, zip(*data)))
    parallel=Parallel()
    parallel_axis = []
    for i in range(len(Label)):
        parallel_axis.append({"dim":i,"name":Label[i]})
    parallel.add_schema(schema=parallel_axis)
    parallel.add("",data,is_smooth=True)
    parallel.set_global_opts(
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
    grid0 = Grid(init_opts=opts.InitOpts(
        width="100%",
        height="100%",
        renderer=globals.RenderType.SVG, ))
    grid0.add(bar1, grid_opts={'left': '20%', 'bottom': '34%'})
    option0 = grid0.dump_options_with_quotes()
    option0 = json.loads(option0)
    grid = Grid(init_opts=opts.InitOpts(
        width="100%",
        height="100%",
        renderer=globals.RenderType.SVG, ))
    grid.add(bar2, grid_opts={'left': '15%', 'bottom': '50%'})
    option1 = grid.dump_options_with_quotes()
    option1 = json.loads(option1)
    grid1 = Grid(init_opts=opts.InitOpts(
        width="100%",
        height="100%",
        renderer=globals.RenderType.SVG, ))
    grid1.add(parallel, grid_opts={'left': '30%', 'bottom': '34%'})
    option2 = grid1.dump_options_with_quotes()
    option2 = json.loads(option2)

    option = {"option": [option1,option2], "query": query}
    return option
