import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.set_page_config(page_title="Radar de Oportunidades", layout="wide")
st.title("🚀 Mi Monitor de Trading Permanente")

# Lista de activos estrella
tickers = ["SPY", "MELI", "ASML", "CRWD", "BTC-USD", "NVDA", "AAPL", "MSFT", "MSTR", "TSLA"]

@st.cache_data(ttl=300)
def get_data_fast(symbols):
    # Descarga masiva de datos de cierre
    df = yf.download(symbols, period="60d", interval="1d", progress=False)
    return df['Close']

try:
    with st.spinner('Sincronizando con el mercado...'):
        prices = get_data_fast(tickers)
        results = []
        
        for t in tickers:
            try:
                # Extraer serie de precios para el ticket actual
                serie_precios = prices[t].dropna()
                if len(serie_precios) > 15:
                    rsi = ta.rsi(serie_precios, length=14)
                    if rsi is not None and not rsi.empty:
                        last_rsi = float(rsi.iloc[-1])
                        last_price = float(serie_precios.iloc[-1])
                        
                        results.append({
                            "Ticket": t,
                            "Precio": round(last_price, 2),
                            "RSI": round(last_rsi, 2),
                            "Estado": "🔥 Sobrecompra" if last_rsi > 70 else ("🟢 Oportunidad" if last_rsi < 30 else "⚖️ Neutral")
                        })
            except:
                continue # Si uno falla, seguimos con el siguiente

    if results:
        st.subheader("Análisis de Fuerza (RSI)")
        df_final = pd.DataFrame(results)
        
        # Función de estilo actualizada para versiones modernas de Pandas
        def color_estado(val):
            if val == '🟢 Oportunidad': return 'background-color: #d4edda; color: #155724'
            if val == '🔥 Sobrecompra': return 'background-color: #f8d7da; color: #721c24'
            return ''

        st.dataframe(df_final.style.map(color_estado, subset=['Estado']), use_container_width=True)
    else:
        st.warning("Cargando datos iniciales... Si no aparece la tabla, pulsa el botón de Refrescar.")
    
except Exception as e:
    st.error(f"Ajustando conexión... Pulsa Refrescar. (Info: {e})")

if st.button('Refrescar Monitor'):
    st.cache_data.clear()
    st.rerun()

st.info("Datos obtenidos de Yahoo Finance (Gratis y Permanente).")
