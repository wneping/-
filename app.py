import streamlit as st
import pandas as pd

# ========= 基本設定 =========
st.set_page_config(
    page_title="台股盤後資訊,食安自負",
    layout="wide"
)

# ========= CSV 路徑 =========
CSV_PATH = r"day0222.csv"

# ========= 讀取資料 =========
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip()

    # 移除日期欄位
    if "日期" in df.columns:
        df = df.drop(columns=["日期"])

    # 數字欄位轉換
    numeric_cols = ["成交股數", "成交金額", "開盤價", "最高價", "最低價", "收盤價", "成交筆數"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = (
                df[col].astype(str)
                .str.replace(",", "")
                .str.replace("--", "")
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna()
    return df

df = load_data()

# ========= 左上角標題 =========
st.title("當日成交資訊查詢")

# ========= 顯示成交筆數前20筆排行榜 =========
st.subheader("成交筆數前20名")
if "成交筆數" in df.columns:
    top20 = df.sort_values("成交筆數", ascending=False).head(20)
else:
    top20 = df.head(20)
st.dataframe(top20, use_container_width=True)

# ========= 中間搜尋區 =========
st.subheader("個別股票查詢")

col1, col2, col3 = st.columns([1,2,1])
with col2:
    # 下拉選單
    stock_list = df["證券代號"].astype(str).unique()
    selected_stock = st.selectbox("選擇股票", stock_list)

    # 輸入股票代號
    search = st.text_input("或輸入股票代號")

# ========= 搜尋邏輯 =========
# 優先使用輸入框，如果輸入了股票代號就用輸入框
if search:
    stock_to_show = str(search)
else:
    stock_to_show = str(selected_stock)

# 篩選資料
query_result = df[df["證券代號"].astype(str) == stock_to_show]

# ========= 顯示查詢結果 =========
st.subheader(f"股票 {stock_to_show} 資料")
if query_result.empty:
    st.warning("查無資料")
else:

    st.dataframe(query_result, use_container_width=True)
