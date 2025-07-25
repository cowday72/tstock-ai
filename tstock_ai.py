import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="台灣股市 AI 預測", layout="centered")

# 股票代號對應表
stock_dict = {
    "2330": "台積電",
    "2317": "鴻海",
    "2603": "長榮",
    "2881": "富邦金",
    "2303": "聯電"，
    "2891"："中信金"
}

# 假財報資料（你日後可用 API 或爬蟲取代）
def get_fake_financials(stock_id):
    return {
        "EPS": round(5 + 2 * (hash(stock_id) % 3), 2),
        "ROE": round(10 + (hash(stock_id) % 10), 2),
        "毛利率": round(40 + (hash(stock_id) % 10), 2),
        "負債比": round(30 + (hash(stock_id) % 20), 2)
    }

# AI 預測邏輯（簡化版）
def predict_stock_up(fin):
    score = 0
    if fin["EPS"] > 6: score += 1
    if fin["ROE"] > 15: score += 1
    if fin["毛利率"] > 45: score += 1
    if fin["負債比"] < 40: score += 1
    return score / 4

# Streamlit UI
st.title("📈 台灣股市 AI 預測系統")
stock_id = st.selectbox("選擇股票代號", list(stock_dict.keys()), format_func=lambda x: f"{x} {stock_dict[x]}")

# 顯示財報
fin = get_fake_financials(stock_id)
st.subheader("📊 財報指標（模擬）")
st.write(fin)

# 顯示預測
prob = predict_stock_up(fin)
st.subheader("🔮 AI 預測結果")
st.metric(label="預測未來30天股價上漲機率", value=f"{round(prob * 100, 1)}%")

# 顯示股價趨勢圖
st.subheader("📉 最近30天股價走勢")
ticker = yf.Ticker(f"{stock_id}.TW")
hist = ticker.history(period="1mo")
if not hist.empty:
    st.line_chart(hist["Close"])
else:
    st.warning("找不到該股票的近期股價資料。")
