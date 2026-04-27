import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.set_page_config(page_title="Radar S&P 500 Profesional", layout="wide")
st.title("📊 Monitor RSI S&P 500")

# 1. Obtener los Tickers (Con nombres seguros para Yahoo)
@st.cache_data(ttl=3600)
def get_sp500_tickers():
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        df = pd.read_html(url)[0]
        # Cambiamos puntos por guiones (ej. BRK.B -> BRK-B) que es como los usa Yahoo
        return df['Symbol'].str.replace('.', '-', regex=True).tolist()
    except:
        return ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "SPY"]

# 2. Descarga y Procesamiento
def fetch_market_data():
    tickers = get_sp500_tickers()
    results = []
    
    status = st.empty()
    progress = st.progress(0)
    
    # Intentamos descargar todo en un solo bloque (Más rápido si funciona)
    status.info("Conectando con el mercado... por favor espera.")
    try:
        # Pedimos solo el último mes para que la carga sea ligera
        data = yf.download(tickers, period="30d", interval="1d", progress=False)['Close']
        
        for i, ticker in enumerate(tickers):
            try:
                # Extraemos la serie de precios de la columna correspondiente
                serie = data[ticker].dropna()
                if len(serie) > 14:
                    rsi = ta.rsi(serie, length=14)
                    if rsi is not None and not rsi.empty:
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
            
            # Actualizar barra de progreso visualmente
            if i % 50 == 0:
                progress.progress(i / len(tickers))
                
    except Exception as e:
        st.error(f"Error de conexión con Yahoo: {e}")
        return pd.DataFrame()

    progress.empty()
    status.success("✅ Análisis completo.")
    return pd.DataFrame(results)

# --- INTERFAZ ---

if 'market_data' not in st.session_state:
    st.session_state.market_data = pd.DataFrame()

if st.button('🚀 ESCANEAR S&P 500 AHORA') or st.session_state.market_data.empty:
    st.session_state.market_data = fetch_market_data()

df = st.session_state.market_data

if not df.empty:
    # Métricas superiores
    m1, m2, m3 = st.columns(3)
    m1.metric("Empresas Analizadas", len(df))
    m2.metric("🟢 En Oportunidad", len(df[df['Estado'] == "🟢 Oportunidad"]))
    m3.metric("🔥 En Sobrecompra", len(df[df['Estado'] == "🔥 Sobrecompra"]))

    # Filtro y Tabla
    search = st.text_input("Filtrar por nombre (ej: NVDA):").upper()
    if search:
        df = df[df['Ticket'].str.contains(search)]

    # Ordenar por RSI más bajo automáticamente
    st.dataframe(df.sort_values(by="RSI"), use_container_width=True)
else:
    st.warning("No se pudieron obtener datos. Esto suele pasar si Yahoo Finance está saturado. Intenta darle al botón de Escanear de nuevo en un momento.")
