import pyecharts.options as opts
from pyecharts.charts import Bar, Line

"""
Gallery 使用 pyecharts 1.1.0
参考地址: https://www.echartsjs.com/examples/editor.html?c=mix-line-bar

目前无法实现的功能:

1、暂无
"""
def TREND_render(x,y,z,y_up,y_down,max_index,min_index,x_name,y_name,query,answer,up_count,down_count):
    bar = (
        Bar()
            .add_xaxis(xaxis_data=x)
            .add_yaxis(
            series_name="",
            yaxis_data=y,
            stack="GDP",
            itemstyle_opts=opts.ItemStyleOpts(color="rgba(0,0,0,0)"),

        )
            .add_yaxis(series_name="increase", yaxis_data=y_up, stack="GDP",markpoint_opts=opts.MarkPointOpts(
            data=[opts.MarkPointItem(name=x[max_index], coord=[x[max_index], y[max_index]+y_up[max_index]+z[max_index]], value="Max")]
        ),)
            .add_yaxis(series_name="decrease", yaxis_data=y_down, stack="GDP",markpoint_opts=opts.MarkPointOpts(
            data=[opts.MarkPointItem(name=x[min_index], coord=[x[min_index], y[min_index]+y_down[min_index]+z[max_index]], value="Max")]
        ),)
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                name=y_name,
                type_="value",
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                min_=int(min(y)-(max(y)-min(y))/10)
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
            text=['\n'+"Q:"+' '+query+'\n'+'A:'+' '+answer],
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
            series_name='',
            yaxis_index=0,
            y_axis=y,
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                # data=[opts.MarkPointItem(name=x[index], coord=[x[index], y[index]], value=y[index])]
            ),
        )

        .set_global_opts(legend_opts=opts.LegendOpts(is_show=False),)
    )
    # line.overlap(bar).render("TREND.html")
    bar.overlap(line).render("TREND.html")