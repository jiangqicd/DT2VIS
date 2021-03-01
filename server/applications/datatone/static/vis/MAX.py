import pyecharts.options as opts
from pyecharts.charts import Line,Grid
from pyecharts.faker import Faker
def find_extremum_render(x,y,index,x_name,y_name,query,answer):
    line=Line()
    line.add_xaxis(x)
    line.add_yaxis(
        y_name,
        y_axis=y,
        markpoint_opts=opts.MarkPointOpts(
            data=[opts.MarkPointItem(name=x[index], coord=[x[index], y[index]], value="Min", itemstyle_opts=opts.ItemStyleOpts(opacity=0.6))]
        ),
    )
    line.set_global_opts(
        yaxis_opts=opts.AxisOpts(min_=int(min(y)-(max(y)-min(y))/10),name=y_name),
        legend_opts=opts.LegendOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate":40,'interval':0,'show':True},name=x_name),
        graphic_opts=[opts.GraphicText(
          graphic_item=opts.GraphicItem(
              left="center",
              top="bottom",
              z=100,
        ),
          graphic_textstyle_opts=opts.GraphicTextStyleOpts(
            text=["Q:"+' '+query+'\n'+'\n'+'A:'+' '+answer],
            font="14px Microsoft YaHei",
            graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                fill="#333"
            )
        )
    )]

    )
    grid = Grid()
    grid.add(line,  grid_opts={'left':'20%','bottom':'35%' })
    grid.render("../vis/MAX.html")
    vis_path="../vis/MAX.html"
    return vis_path
