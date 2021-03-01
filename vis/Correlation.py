from pyecharts import options as opts
from pyecharts.charts import Boxplot,Grid,Bar,Line,Scatter
from pyecharts.globals import ThemeType
import operator
from pyecharts import globals
import json
from pyecharts.commons.utils import JsCode
import numpy as np
def find_correlation_render(attributes,data, pearsonr,query,table_path,answer):
    dimensions=len(attributes)
    if dimensions==2:
        data[0]=list(map(str,data[0]))
        data[1] = list(map(float, data[0]))
        l1_1=Scatter()
        l1_1.add_xaxis(data[0])
        l1_1.add_yaxis("",data[1])
        l1_1.set_global_opts(
            datazoom_opts=opts.DataZoomOpts(),
            xaxis_opts=opts.AxisOpts(
                name=attributes[0]
            ),
            yaxis_opts=opts.AxisOpts(
                name=attributes[1]
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
        grid.add(l1_1,  grid_opts={'left':'15%','bottom':'34%'})
        option1=grid.dump_options_with_quotes()
        option1=json.loads(option1)
        option={"option":[option1],"query":query}
        return option
    elif dimensions==3:
        l1_1=Scatter()
        data[0]=list(map(str,data[0]))
        data[1] = list(map(float, data[1]))
        data[2] = list(map(float, data[2]))
        l1_1.add_xaxis(data[0])
        l1_1.add_yaxis("",data[1])
        l1_1.set_global_opts(
            datazoom_opts=opts.DataZoomOpts(),
            xaxis_opts=opts.AxisOpts(
                name=attributes[0],
                axislabel_opts=opts.LabelOpts(rotate=50, interval=0),
                grid_index=0,
            ),
            yaxis_opts=opts.AxisOpts(
                name=attributes[1],
                grid_index=0,
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
        l1_2=Scatter()
        l1_2.add_xaxis(data[0])
        l1_2.add_yaxis("",data[2])
        l1_2.set_global_opts(
            datazoom_opts=opts.DataZoomOpts(),
            xaxis_opts=opts.AxisOpts(
                name=attributes[0],
                axislabel_opts=opts.LabelOpts(rotate=50, interval=0),
                grid_index=1,
            ),
            yaxis_opts=opts.AxisOpts(
                name=attributes[2],
                grid_index=1
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
        data[1] = list(map(str, data[1]))
        l2_1=Scatter()
        l2_1.add_xaxis(data[1])
        l2_1.add_yaxis("",data[2])
        l2_1.set_global_opts(
            datazoom_opts=opts.DataZoomOpts(),
            xaxis_opts=opts.AxisOpts(
                name=attributes[0],
                axislabel_opts=opts.LabelOpts(rotate=50, interval=0),
                grid_index=2
            ),
            yaxis_opts=opts.AxisOpts(
                name=attributes[1],
                grid_index=2
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
        grid.add(
          chart=l1_1,
          grid_opts=opts.GridOpts(pos_right="57%", pos_bottom="20%",pos_top="40%"),
          grid_index=0,
        )
        grid.add(
          chart=l1_2,
          grid_opts=opts.GridOpts(pos_left="57%", pos_bottom="20%",pos_top="40%"),
          grid_index=1,
        )
        grid.add(
            chart=l2_1,
            grid_opts=opts.GridOpts(pos_right="57%", pos_bottom="60%"),
            grid_index=2,
        )
        option1=grid.dump_options_with_quotes()
        option1=json.loads(option1)
        option={"option":[option1],"query":query}
        return option
    elif dimensions==4:
        data[0]=list(map(str,data[0]))
        data[1] = list(map(float, data[1]))
        data[2] = list(map(float, data[2]))
        data[3] = list(map(float, data[3]))
        l1_1=Scatter()
        l1_1.add_xaxis(data[0])
        l1_1.add_yaxis("",data[1])
        l1_1.set_global_opts(
            datazoom_opts=opts.DataZoomOpts(),
            xaxis_opts=opts.AxisOpts(
                name=attributes[0],
                axislabel_opts=opts.LabelOpts(rotate=50, interval=0),
                grid_index=0,
            ),
            yaxis_opts=opts.AxisOpts(
                name=attributes[1],
                grid_index=0,
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
        l1_2=Scatter()
        l1_2.add_xaxis(data[0])
        l1_2.add_yaxis("",data[2])
        l1_2.set_global_opts(
            datazoom_opts=opts.DataZoomOpts(),
            xaxis_opts=opts.AxisOpts(
                name=attributes[0],
                axislabel_opts=opts.LabelOpts(rotate=50, interval=0),
                grid_index=1,
            ),
            yaxis_opts=opts.AxisOpts(
                name=attributes[2],
                grid_index=1
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
        l2_1=Scatter()
        l2_1.add_xaxis(data[0])
        l2_1.add_yaxis("",data[3])
        l2_1.set_global_opts(
            datazoom_opts=opts.DataZoomOpts(),
            xaxis_opts=opts.AxisOpts(
                name=attributes[0],
                axislabel_opts=opts.LabelOpts(rotate=50, interval=0),
                grid_index=2
            ),
            yaxis_opts=opts.AxisOpts(
                name=attributes[3],
                grid_index=2
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
        data[1] = list(map(str, data[1]))
        l2_2=Scatter()
        l2_2.add_xaxis(data[1])
        l2_2.add_yaxis("",data[2])
        l2_2.set_global_opts(
            datazoom_opts=opts.DataZoomOpts(),
            xaxis_opts=opts.AxisOpts(
                name=attributes[1],
                axislabel_opts=opts.LabelOpts(rotate=50, interval=0),
                grid_index=3
            ),
            yaxis_opts=opts.AxisOpts(
                name=attributes[2],
                grid_index=3
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
        grid.add(
          chart=l1_1,
          grid_opts=opts.GridOpts(pos_right="57%", pos_bottom="20%",pos_top="40%"),
          grid_index=0,
        )
        grid.add(
          chart=l1_2,
          grid_opts=opts.GridOpts(pos_left="57%", pos_bottom="20%",pos_top="40%"),
          grid_index=1,
        )
        grid.add(
            chart=l2_1,
            grid_opts=opts.GridOpts(pos_right="57%", pos_bottom="60%"),
            grid_index=2,
        )
        grid.add(
            chart=l2_2,
            grid_opts=opts.GridOpts(pos_left="57%", pos_bottom="60%"),
            grid_index=3,
        )
        r1_1=Scatter()
        r1_1.add_xaxis(data[1])
        r1_1.add_yaxis("",data[3]
        )
        r1_1.set_global_opts(
            datazoom_opts=opts.DataZoomOpts(),
            xaxis_opts=opts.AxisOpts(
                name=attributes[1],
                axislabel_opts=opts.LabelOpts(rotate=50, interval=0),
                grid_index=0
            ),
            yaxis_opts=opts.AxisOpts(
                name=attributes[3],
                grid_index=0
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
        data[2] = list(map(str, data[2]))
        r1_2=Scatter()
        r1_2.add_xaxis(data[2])
        r1_2.add_yaxis("",data[3]
        )
        r1_2.set_global_opts(
            datazoom_opts=opts.DataZoomOpts(),
            xaxis_opts=opts.AxisOpts(
                name=attributes[2],
                axislabel_opts=opts.LabelOpts(rotate=50, interval=0),
                grid_index=1
            ),
            yaxis_opts=opts.AxisOpts(
                name=attributes[3],
                grid_index=1
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
        grid1 = Grid(init_opts=opts.InitOpts(
            width="100%",
            height="100%",
            renderer=globals.RenderType.SVG, ))
        grid1.add(
            chart=r1_1,
            grid_opts=opts.GridOpts(pos_right="57%", pos_bottom="30%"),
            grid_index=0,
        )
        grid1.add(
            chart=r1_2,
            grid_opts=opts.GridOpts(pos_left="57%", pos_bottom="30%"),
            grid_index=1,
        )
        option1=grid.dump_options_with_quotes()
        option1=json.loads(option1)
        option2=grid1.dump_options_with_quotes()
        option2=json.loads(option2)
        option={"option":[option1,option2],"query":query}
        return option