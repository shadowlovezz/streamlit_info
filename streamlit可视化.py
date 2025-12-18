import json
import pandas as pd
import streamlit as st
import streamlit_echarts as ste
from PIL import Image
from pyecharts import options as opts
from pyecharts.charts import Bar, Map, Liquid
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType

st.set_page_config(page_title="猎职图鉴", layout="wide")

# ---------- 缓存：避免交互时反复读文件 ----------
@st.cache_data
def load_china_geojson(path="./china.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.loads(f.read())

@st.cache_data
def load_jobs(path="./相关岗位样例.csv"):
    return pd.read_csv(path, encoding="GBK")

@st.cache_data
def load_wordcloud(path="./cloudfinal.png"):
    return Image.open(path)

china_geojson = load_china_geojson()
china_map = ste.Map("china", china_geojson)

data = load_jobs()
df = data[["职位", "地区", "要求"]].copy()
wordcloud_img = load_wordcloud()

# ---------- 侧边栏筛选器（核心体验） ----------
st.sidebar.header("筛选器")
kw = st.sidebar.text_input("职位关键词（可空）", "")
regions = sorted(df["地区"].dropna().unique().tolist())
sel_regions = st.sidebar.multiselect("地区", regions, default=regions[:5] if len(regions) > 5 else regions)

mask = df["地区"].isin(sel_regions) if sel_regions else True
if kw.strip():
    mask = mask & df["职位"].astype(str).str.contains(kw.strip(), case=False, na=False)
df_f = df[mask]

# ---------- 标题与KPI ----------
st.title("猎职图鉴")
st.caption("大数据相关岗位信息可视化：分布、产业结构与岗位样例检索")

k1, k2, k3 = st.columns(3)
k1.metric("筛选后岗位数", f"{len(df_f):,}")
k2.metric("覆盖地区数", f"{df_f['地区'].nunique():,}")
top_region = df_f["地区"].value_counts().index[0] if len(df_f) else "—"
k3.metric("Top 地区", top_region)

st.divider()

# ---------- Tabs：把页面变“有层级” ----------
tab1, tab2, tab3 = st.tabs(["总览", "产业结构", "岗位样例"])

with tab1:
    # 你的地图 dt（建议把标题改成“产值分布”或把数据改成岗位数）
    dt = (
        Map()
        .add("产值", [...], "china")  # 这里保留你原来的省份数据
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="（建议改名）大数据相关产值分布"),
            visualmap_opts=opts.VisualMapOpts(max_=30000000),
        )
    )

    left, right = st.columns([1.2, 1])
    with left:
        st.subheader("空间分布")
        ste.st_pyecharts(dt, map=china_map)
    with right:
        st.subheader("岗位样例（筛选后）")
        st.dataframe(df_f, use_container_width=True, height=520)

with tab2:
    x_data = ["软件产品", "信息技术服务", "信息安全", "嵌入式系统软件", "软件业务出口", "利润总额"]

    bar = (
        Bar({"theme": ThemeType.PURPLE_PASSION})
        .add_xaxis(x_data)
        .add_yaxis("本期累计", [26583, 70128, 2038, 9376, 524, 12648], label_opts=opts.LabelOpts(is_show=False))
        .add_yaxis("同期累计", [24179, 62777, 1847, 8425, 509, 11986], label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True, trigger="axis", axis_pointer_type="cross"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
        )
    )

    liqud = (
        Liquid()
        .add(
            "产值增比", [0.112],
            label_opts=opts.LabelOpts(
                font_size=30,
                formatter=JsCode("""function (param) {return (Math.floor(param.value * 10000) / 100) + '%';}"""),
                position="inside",
            )
        )
    )

    c1, c2, c3 = st.columns([1.2, 0.8, 1])
    with c1:
        st.subheader("产业结构对比")
        ste.st_pyecharts(bar)
    with c2:
        st.subheader("产值增比")
        ste.st_pyecharts(liqud)
    with c3:
        st.subheader("岗位要求词云")
        st.image(wordcloud_img, use_container_width=True)

with tab3:
    st.subheader("岗位详情检索")
    st.dataframe(df_f, use_container_width=True)
    with st.expander("口径说明/数据来源", expanded=False):
        st.write("这里放数据来源、字段定义、更新时间等。")
