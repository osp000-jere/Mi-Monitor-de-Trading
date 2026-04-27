import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.set_page_config(page_title="Radar S&P 500", layout="wide")
st.title("📊 Monitor RSI S&P 500")

# --- FUNCIÓN PARA OBTENER TICKERS DEL S&P 500 ---
@st.cache_data
def get_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    table = pd.read_html(url)
    df = table[0]
    return df['Symbol'].tolist()

# --- FUNCIÓN PARA DESCARGAR DATOS CON CACHÉ ---
@st.cache_data(ttl=600) # Se actualiza cada 10 minutos
def download_all_data(tickers):
    data = yf.download(tickers, period="60d", interval="1d", progress=False)['Close']
    return data

try:
    tickers = get_sp500_tickers()
    
    with st.spinner(f'Analizando {len(tickers)} acciones... esto tardará unos 45 segundos la primera vez.'):
        prices = download_all_data(tickers)
        
        results = []
        for t in tickers:
            try:
                serie = prices[t].dropna()
                if len(serie) > 14:
                    rsi = ta.rsi(serie, length=14)
                    last_rsi = rsi.iloc[-1]
                    last_price = serie.iloc[-1]
                    
                    results.append({
                        "Ticket": t,
                        "Precio": round(last_price, 2),
                        "RSI": round(last_rsi, 2),
                        "Estado": "🔥 Sobrecompra" if last_rsi > 70 else ("🟢 Oportunidad" if last_rsi < 30 else "⚖️ Neutral")
                    })
            except:
                continue

    if results:
        df = pd.DataFrame(results)
        
        # Filtros rápidos
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Acciones", len(df))
        with col2:
            st.metric("En Sobreventa (Oportunidad)", len(df[df['Estado'] == "🟢 Oportunidad"]))
        with col3:
            st.metric("En Sobrecompra", len(df[df['Estado'] == "🔥 Sobrecompra"]))

        st.subheader("Buscador y Resultados")
        search = st.text_input("Filtrar por Ticket (ej: AAPL, TSLA):").upper()
        if search:
            df = df[df['Ticket'].str.contains(search)]

        st.dataframe(df.sort_values(by="RSI", ascending=True), use_container_width=True)

except Exception as e:
    st.error("Error al cargar el S&P 500. Reintenta en unos segundos.")

if st.button('Actualizar Datos'):
    st.cache_data.clear()
    st.rerun()
