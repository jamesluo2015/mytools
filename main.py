import pandas as pd
import streamlit as st
from utils import dataframe_agent


def create_chart(input_data, chart_type):
    df_data = pd.DataFrame(input_data["data"], columns=input_data["columns"])
    df_data.set_index(input_data["columns"][0], inplace=True)
    if chart_type == "bar":
        st.bar_chart(df_data)
    elif chart_type == "line":
        st.line_chart(df_data)
    elif chart_type == "scatter":
        st.scatter_chart(df_data)

st.title("小工同学")

# with st.sidebar:
openai_api_key = st.text_input("请输入阿里百炼API密钥：", type="password")
# st.markdown("[获取阿里 百炼 API key](https://platform.openai.com/account/api-keys)")
st.write("sk-5e17dee3228646c18589922b39997f38")

data = st.file_uploader("上传excle格式文件：", type=["xls","xlsx"])
if data:
    st.session_state["df"] = pd.read_excel(data)
    with st.expander("底表数据"):
        st.dataframe(st.session_state["df"])


query = st.text_area("请输入以上表格内容的问题，或数据提取请求，或可视化要求（支持散点图、折线图、条形图）：")
button = st.button("获取回答")

if button and not openai_api_key:
    st.warning("请输入你的阿里百炼 API密钥")
    st.stop()
if button and not query:
    st.warning("请输入你的问题")
    st.stop()
if button and "df" not in st.session_state:
    st.warning("请先上传数据文件")
    st.stop()
if button and openai_api_key and "df" in st.session_state  and query:
    with st.spinner("小工正在努力中，请稍等..."):
        response_dict = dataframe_agent(openai_api_key, st.session_state["df"], query)
        if "answer" in response_dict:
            st.write(response_dict["answer"])
        if "table" in response_dict:
            st.table(pd.DataFrame(response_dict["table"]["data"],
                                  columns=response_dict["table"]["columns"]))
        if "bar" in response_dict:
            create_chart(response_dict["bar"], "bar")
        if "line" in response_dict:
            create_chart(response_dict["line"], "line")
        if "scatter" in response_dict:
            create_chart(response_dict["scatter"], "scatter")
