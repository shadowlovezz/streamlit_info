import json
import streamlit_echarts as ste
import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import plotly.express
from pyecharts import options as opts
from pyecharts.charts import Bar,Map,Line,Liquid,Scatter
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType

st.set_page_config(page_title="猎职图鉴",layout="wide")

with open("./china.json", "r", encoding="utf-8") as f:
    map = ste.Map("china", json.loads(f.read()),)
dt=(
    Map()
    .add("产值",
         [['北京',31626607],['天津',1962241],['河北',451627],['上海',11875920],['江苏',18796207],['浙江',12702283],
          ['福建',3012351],['山东',14804387],['广东',27138686],['海南',71239],['山西',73462],['安徽',608469],['江西',340899],
          ['河南',535728],['湖北',2139453],['湖南',1065716],['内蒙古',6083],['广西',714530],['重庆',2762589],['四川',6722325],
          ['贵州',1078845],['云南',71020],['西藏',0],['陕西',3400700],['甘肃',33253],['青海',2845],['宁夏',88874],['新疆',35221],
          ['辽宁',2241320],['吉林',212194],['黑龙江',35946]],"china")
    .set_series_opts(
        label_opts=opts.LabelOpts(is_show=False)
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="大数据相关岗位分布"),
        visualmap_opts=opts.VisualMapOpts(max_=30000000),
    )
)

x_data = ["软件产品", "信息技术服务", "信息安全", "嵌入式系统软件", "软件业务出口", "利润总额"]
bar=(
    Bar({"theme":ThemeType.PURPLE_PASSION})
    .add_xaxis(xaxis_data=x_data)
    .add_yaxis(
        series_name="本期累计",
        y_axis=[26583, 70128, 2038,9376,524,12648],
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_yaxis(
        series_name="同期累计",
        y_axis=[24179,62777,1847,8425,509,11986],
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            is_show=True, trigger="axis", axis_pointer_type="cross"
        ),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
            axislabel_opts=opts.LabelOpts(rotate=-15),
        ),
    )
)

line = (
    Line({"theme":ThemeType.PURPLE_PASSION})
    .add_xaxis(xaxis_data=x_data)
    .add_yaxis(
        series_name="同比增减%",
        y_axis=[9.9,11.7,10.4,10.4,11.3,3.0,5.7],
        label_opts=opts.LabelOpts(is_show=False),
    )
)

scatter=(
    Scatter({"theme":ThemeType.PURPLE_PASSION})
    .add_xaxis(xaxis_data=x_data)
    .add_yaxis("本期累计",[26583, 70128, 2038,9376,524,12648],
               label_opts=opts.LabelOpts(is_show=False),)
    .add_yaxis("同期累计",[24179,62777,1847,8425,509,11986],
               label_opts=opts.LabelOpts(is_show=False),)
)

liqud=(
    Liquid()
    .add("lq",[0.112],
         label_opts=opts.LabelOpts(
             font_size=30,
             formatter=JsCode(
                 """function (param) {
                     return (Math.floor(param.value * 10000) / 100) + '%';
                 }"""
             ),
             position="inside",
         ),
         )
)

image=Image.open("./cloudfinal.png")

data=pd.read_csv(r'./相关岗位样例.csv', encoding="GBK")
df=data[["职位","地区","要求"]]

c11,c12=st.columns([1,2])
with c11:
    st.subheader("大数据相关岗位产值统计")
    ste.st_pyecharts(dt,map=map)
with c12:
    st.subheader("大数据相关岗位信息")
    st.write(df)
c21,c22,c23=st.columns([1.2,0.9,0.9])
with c21:
    st.subheader("大数据相关产值现状")
    ste.st_pyecharts(bar)
with c22:
    st.subheader("大数据相关产值增比")
    ste.st_pyecharts(liqud)
with c23:
    st.subheader("大数据岗位要求词云图")
    st.image(image)