import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.set_page_config(page_title="Radar de Oportunidades", layout="wide")
st.title("🚀 Mi Monitor de Trading Permanente")

# Tus activos favoritos
tickers = ["ASML", "CRWD", "MELI", "BTC-USD", "MSTR", "ORCL", "PYPL", "MSFT", "TTD", "SPY"]

def get_data(ticker):
    df = yf.download(ticker, period="1y", interval="1d")
    df['RSI'] = ta.rsi(df['Close'], length=14)
    df['MA20'] = ta.sma(df['Close'], length=20)
    return df.iloc[-1]

st.subheader("Estado del Mercado en Tiempo Real")
data_list = []
for t in tickers:
    try:
        last_row = get_data(t)
        data_list.append({
            "Ticket": t,
            "Precio": round(float(last_row['Close']), 2),
            "RSI": round(float(last_row['RSI']), 2),
            "Punto Inflexión (MA20)": round(float(last_row['MA20']), 2),
            "Estado": "🔥 Sobrecompra" if last_row['RSI'] > 70 else ("🟢 Oportunidad" if last_row['RSI'] < 30 else "⚖️ Neutral")
        })
    except:
        pass

st.table(pd.DataFrame(data_list))
