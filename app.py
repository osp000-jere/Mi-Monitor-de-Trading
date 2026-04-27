import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.set_page_config(page_title="Radar de Oportunidades", layout="wide")
st.title("🚀 Mi Monitor de Trading Permanente")

# Lista de activos
tickers = ["ASML", "CRWD", "MELI", "BTC-USD", "MSTR", "ORCL", "PYPL", "MSFT", "TTD", "SPY"]

def get_data(ticker):
    try:
        # Descargamos datos (1 año para tener suficiente historial para el RSI)
        df = yf.download(ticker, period="1y", interval="1d", progress=False)
        if df.empty:
            return None
        
        # Calculamos RSI
        df['RSI'] = ta.rsi(df['Close'], length=14)
        # Media Móvil de 20 días
        df['MA20'] = ta.sma(df['Close'], length=20)
        
        last_row = df.iloc[-1]
        
        return {
            "Ticket": ticker,
            "Precio": round(float(last_row['Close']), 2),
            "RSI": round(float(last_row['RSI']), 2),
            "Punto Inflexión (MA20)": round(float(last_row['MA20']), 2),
            "Estado": "🔥 Sobrecompra" if last_row['RSI'] > 70 else ("🟢 Oportunidad" if last_row['RSI'] < 30 else "⚖️ Neutral")
        }
    except Exception as e:
        return None

# Botón para actualizar manualmente
if st.button('Actualizar Datos'):
    st.rerun()

st.subheader("Estado del Mercado")

results = []
# Usamos una barra de progreso para saber que está trabajando
with st.spinner('Cargando datos de Yahoo Finance...'):
    for t in tickers:
        data = get_data(t)
        if data:
            results.append(data)

if results:
    df_final = pd.DataFrame(results)
    # Mostramos la tabla con colores según el estado
    st.dataframe(df_final.style.applymap(
        lambda x: 'background-color: #d4edda' if x == '🟢 Oportunidad' else ('background-color: #f8d7da' if x == '🔥 Sobrecompra' else ''),
        subset=['Estado']
    ), use_container_width=True)
else:
    st.error("No se pudieron cargar los datos. Revisa la conexión o los tickers.")

st.info("Nota: Los datos pueden tener un retraso de 15 minutos según Yahoo Finance.")st))
