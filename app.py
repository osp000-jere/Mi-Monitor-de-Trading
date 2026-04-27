import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.set_page_config(page_title="Radar de Oportunidades", layout="wide")
st.title("🚀 Mi Monitor de Trading Permanente")

# Lista reducida para probar que arranque rápido
tickers = ["SPY", "MELI", "ASML", "CRWD", "BTC-USD", "NVDA", "AAPL", "MSFT"]

@st.cache_data(ttl=300) # Guarda los datos por 5 minutos para que sea veloz
def get_data_fast(symbols):
    # Descarga masiva en una sola petición (mucho más rápido)
    data = yf.download(symbols, period="60d", interval="1d", progress=False)['Close']
    return data

try:
    with st.spinner('Sincronizando con el mercado...'):
        prices = get_data_fast(tickers)
        
        results = []
        for t in tickers:
            # Calculamos RSI sobre los precios descargados
            serie_precios = prices[t]
            rsi = ta.rsi(serie_precios, length=14)
            
            if rsi is not None:
                last_rsi = rsi.iloc[-1]
                last_price = serie_precios.iloc[-1]
                
                results.append({
                    "Ticket": t,
                    "Precio": round(float(last_price), 2),
                    "RSI": round(float(last_rsi), 2),
                    "Estado": "🔥 Sobrecompra" if last_rsi > 70 else ("🟢 Oportunidad" if last_rsi < 30 else "⚖️ Neutral")
                })

    if results:
        st.subheader("Análisis de Fuerza (RSI)")
        df = pd.DataFrame(results)
        st.dataframe(df.style.applymap(
            lambda x: 'background-color: #d4edda' if x == '🟢 Oportunidad' else ('background-color: #f8d7da' if x == '🔥 Sobrecompra' else ''),
            subset=['Estado']
        ), use_container_width=True)
    
except Exception as e:
    st.error(f"Esperando conexión... Reintenta en unos segundos. (Error: {e})")

if st.button('Refrescar Monitor'):
    st.cache_data.clear()
    st.rerun()
