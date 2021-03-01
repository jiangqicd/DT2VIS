from pyecharts import options as opts
from pyecharts.charts import Boxplot,Grid,Bar,Line,Radar
from pyecharts import globals
from pyecharts.globals import ThemeType
import operator
import json
from pyecharts.commons.utils import JsCode
import numpy as np
def find_difference_render(data,X,query,table_path,answer):
    colorList = ['#f36c6c', '#e6cf4e', '#20d180', '#0093ff',"#ca8622","#726930",]
    if len(data)==2:
        bar1=Bar()
        bar1.add_xaxis(X[1])
        bar1.add_yaxis("",data[0][1],label_opts=opts.LabelOpts(position="insideLeft"))
        bar1.reversal_axis()
        bar1.set_global_opts(
            xaxis_opts=opts.AxisOpts(
                position="top"
            ),
            yaxis_opts=opts.AxisOpts(
                is_inverse=True
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
        bar2=Bar()
        bar2.add_xaxis(X[1])
        bar2.add_yaxis("",data[1][1],label_opts=opts.LabelOpts(position="insideRight"))
        bar2.reversal_axis()
        bar2.set_global_opts(
            xaxis_opts=opts.AxisOpts(
                position="top",
                is_inverse=True
            ),
            yaxis_opts=opts.AxisOpts(
                is_inverse=True,
                position="right"
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
        grid1 = Grid(init_opts=opts.InitOpts(
            width="100%",
            height="100%",
            renderer=globals.RenderType.SVG, ) )
        grid1.add(bar1, grid_opts=opts.GridOpts(
            pos_left="60%",pos_bottom="30%"
        ))
        grid1.add(bar2, grid_opts=opts.GridOpts(
            pos_right="60%",pos_bottom="30%"
        ))
        grid1.render("a.html")
        option1 = grid1.dump_options_with_quotes()
        option1 = json.loads(option1)
        lable=[]
        for i in range(len(X[1])):
            lable.append(opts.RadarIndicatorItem(name=X[1][i]))
        # r_data=[]
        # for record in data:
        #     r_data.append(record[1])
        radar=Radar(init_opts=opts.InitOpts(bg_color="#CCCCCC"))
        radar.add_schema(
            schema=lable,
            splitarea_opt=opts.SplitAreaOpts(
               is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
             ),
            textstyle_opts=opts.TextStyleOpts(color="#fff"),
        )
        for i in range(len(data)):
            radar.add(
                series_name=data[i][0],
                data=[data[i][1]],
                linestyle_opts=opts.LineStyleOpts(
                    color=colorList[i],
                    width=3

                )
            )
        radar.set_global_opts(
            graphic_opts=[opts.GraphicText(
                graphic_item=opts.GraphicItem(
                    left="center",
                    top="bottom",
                    z=100,
                ),
                graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                    # 可以通过jsCode添加js代码，也可以直接用字符串
                    text=['\n' + "Q:" + ' ' + query + '\n'+"\n" + 'A:' + ' ' + answer],
                    font="10px Microsoft YaHei",
                    graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                        fill="#333"
                    )
                )
            )]
        )
        grid2 = Grid(init_opts=opts.InitOpts(
            width="100%",
            height="100%",
            renderer=globals.RenderType.SVG, ))
        grid2.add(radar, grid_opts={'left': '20%', 'bottom': '40%',"top":"1%"})
        option2 = grid2.dump_options_with_quotes()
        option2 = json.loads(option2)
        bar3=Bar()
        bar3.add_xaxis(X[1])
        for i in range(len(data)):
            bar3.add_yaxis(data[i][0],data[i][1])
        bar3.set_global_opts(
            xaxis_opts=opts.AxisOpts(
                name=X[0]
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
        grid3 = Grid(init_opts=opts.InitOpts(
            width="100%",
            height="100%",
            renderer=globals.RenderType.SVG, ))
        grid3.add(bar3, grid_opts={'left': '20%', 'bottom': '30%'})
        option3 = grid3.dump_options_with_quotes()
        option3 = json.loads(option3)
        option = {"option": [option1,option2,option3], "query": query}
        return option

    elif len(data)>2 and len(data[0][1])>1:
        lable=[]
        for i in range(len(X[1])):
            lable.append(opts.RadarIndicatorItem(name=X[1][i]))
        # r_data=[]
        # for record in data:
        #     r_data.append(record[1])
        radar=Radar(init_opts=opts.InitOpts(bg_color="#CCCCCC"))
        radar.add_schema(
            schema=lable,
            splitarea_opt=opts.SplitAreaOpts(
               is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
             ),
            textstyle_opts=opts.TextStyleOpts(color="#fff"),
        )
        radar.set_global_opts(
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
        for i in range(len(data)):
            radar.add(
                series_name=data[i][0],
                data=[data[i][1]],
                linestyle_opts=opts.LineStyleOpts(
                    color=colorList[i],
                    width=3

                )
            )

        grid1 = Grid(init_opts=opts.InitOpts(
        width="100%",
        height="100%",
        renderer=globals.RenderType.SVG, ))
        grid1.add(radar, grid_opts={'left': '20%', 'bottom': '30%'})
        option1 = grid1.dump_options_with_quotes()
        option1 = json.loads(option1)
        bar = Bar()
        bar.add_xaxis(X[1])
        for i in range(len(data)):
          bar.add_yaxis(data[i][0], data[i][1])
        bar.set_global_opts(
          xaxis_opts=opts.AxisOpts(
            name=X[0]
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
        grid2 = Grid(init_opts=opts.InitOpts(
        width="100%",
        height="100%",
        renderer=globals.RenderType.SVG, ))
        grid2.add(bar, grid_opts={'left': '20%', 'bottom': '30%'})
        option2 = grid2.dump_options_with_quotes()
        option2 = json.loads(option2)
        option = {"option": [option1,option2], "query": query}
        return option
    elif len(data)>2 and len(data[0][1])==1:
        bar = Bar()
        bar.add_xaxis(X[1])
        for i in range(len(data)):
          bar.add_yaxis(data[i][0], data[i][1])
        bar.set_global_opts(
          xaxis_opts=opts.AxisOpts(
            name=X[0]
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
        grid2 = Grid(init_opts=opts.InitOpts(
        width="100%",
        height="100%",
        renderer=globals.RenderType.SVG, ))
        grid2.add(bar, grid_opts={'left': '20%', 'bottom': '34%'})
        option2 = grid2.dump_options_with_quotes()
        option2 = json.loads(option2)
        option = {"option": [option2], "query": query}
        return option