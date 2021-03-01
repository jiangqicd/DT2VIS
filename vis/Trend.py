import pyecharts.options as opts
from pyecharts.charts import Bar, Line,Grid
import json
from pyecharts import globals
def TREND_render(x,y,z,y_up,y_down,max_index,min_index,x_name,y_name,query,answer):
    x=list(map(str,x))
    y=list(map(float,y))
    bar = (
        Bar()
            .add_xaxis(xaxis_data=x)
            .add_yaxis(
            series_name="increase_value",
            y_axis=y_up,
            stack="GDP",
            markpoint_opts=opts.MarkPointOpts(
            data=[opts.MarkPointItem(type_='max')]
            ),

        )
        #     .add_yaxis(series_name="increase", yaxis_data=y_up, stack="GDP",markpoint_opts=opts.MarkPointOpts(
        #     data=[opts.MarkPointItem(name=x[max_index], coord=[x[max_index], y[max_index]+y_up[max_index]+z[max_index]], value="Max")]
        # ),)
            .add_yaxis(series_name="decrease_value", y_axis=y_down, stack="GDP",markpoint_opts=opts.MarkPointOpts(
            data=[opts.MarkPointItem(type_='max')]
        ),)
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                name=y_name,
                type_="value",
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(name=x_name),
            graphic_opts=[opts.GraphicText(
            graphic_item=opts.GraphicItem(
              left="center",
              top="bottom",
              z=100,
        ),
          graphic_textstyle_opts=opts.GraphicTextStyleOpts(
            # 可以通过jsCode添加js代码，也可以直接用字符串
            text=['\n'+"Q:"+' '+query+'\n'+"\n"+'A:'+' '+answer],
            font="14px Microsoft YaHei",
            graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                fill="#333"
            )
        )
    )]
        )
    )

    line = (
        Line()
            .add_xaxis(xaxis_data=x)
            .add_yaxis(
            series_name='food',
            yaxis_index=0,
            y_axis=y,
            label_opts=opts.LabelOpts(is_show=True),
            # markpoint_opts=opts.MarkPointOpts(
            #     data=[opts.MarkPointItem(type_='max', value='Max'),opts.MarkPointItem(type_='min',value='Max')],
            # ),
        )

        .set_global_opts(legend_opts=opts.LegendOpts(is_show=False),  )
    )
    # line.overlap(bar).render("TREND.html")
    grid = Grid(init_opts=opts.InitOpts(
        width="100%",
        height="100%",
        renderer=globals.RenderType.SVG, ))
    grid.add(bar.overlap(line), grid_opts={'left': '20%', 'bottom': '34%'})
    option1 = grid.dump_options_with_quotes()
    option1 = json.loads(option1)
    option = {"option": [option1], "query": query}
    return option