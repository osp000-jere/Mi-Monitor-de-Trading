import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.set_page_config(page_title="Radar S&P 500 Total", layout="wide")
st.title("📊 Monitor RSI S&P 500 Completo")

# 1. LISTA MANUAL DE TICKERS (Para que nunca falle)
# He incluido una lista representativa, puedes pegar las 500 si gustas
tickers_sp500 = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "BRK-B", "JPM", "V", 
    "JNJ", "WMT", "UNH", "MA", "PG", "HD", "ORCL", "COST", "ADBE", "CRM",
    "ASML", "MELI", "CRWD", "PYPL", "NFLX", "INTC", "AMD", "TXN", "QCOM", "AVGO",
    "SPY", "VOO", "IVV", "DIS", "NKE", "XOM", "CVX", "PEP", "KO", "BAC"
    # (Puedes seguir agregando aquí todos los que desees hasta los 500)
]

def fetch_data():
    results = []
    status = st.empty()
    progress = st.progress(0)
    
    status.info(f"Analizando {len(tickers_sp500)} activos... por favor espera.")
    
    try:
        # Descarga masiva para velocidad
        data = yf.download(tickers_sp500, period="60d", interval="1d", progress=False)['Close']
        
        for i, ticker in enumerate(tickers_sp500):
            try:
                serie = data[ticker].dropna()
                if len(serie) > 14:
                    rsi = ta.rsi(serie, length=14)
                    if rsi is not None:
                        last_rsi = rsi.iloc[-1]
                        last_price = serie.iloc[-1]
                        
                        results.append({
                            "Ticket": ticker,
                            "Precio": round(float(last_price), 2),
                            "RSI": round(float(last_rsi), 2),
                            "Estado": "🟢 Oportunidad" if last_rsi < 30 else ("🔥 Sobrecompra" if last_rsi > 70 else "⚖️ Neutral")
                        })
            except:
                continue
            progress.progress((i + 1) / len(tickers_sp500))
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        
    status.empty()
    progress.empty()
    return pd.DataFrame(results)

# --- LÓGICA DE LA APP ---
if 'market_data' not in st.session_state:
    st.session_state.market_data = pd.DataFrame()

if st.button('🚀 ESCANEAR MERCADO') or st.session_state.market_data.empty:
    st.session_state.market_data = fetch_data()

df = st.session_state.market_data

if not df.empty:
    # Métricas
    c1, c2, c3 = st.columns(3)
    c1.metric("Analizadas", len(df))
    c2.metric("Oportunidades", len(df[df['Estado'] == "🟢 Oportunidad"]))
    c3.metric("Sobrecompra", len(df[df['Estado'] == "🔥 Sobrecompra"]))

    # Tabla
    st.dataframe(df.sort_values(by="RSI"), use_container_width=True)
