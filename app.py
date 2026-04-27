import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.set_page_config(page_title="Radar S&P 500 Multitemporal", layout="wide")
st.title("📊 Monitor RSI: Diario | Semanal | Mensual")

# Lista optimizada de activos
tickers_sp500 = [
    "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "TSLA", "BRK-B", "UNH", "JPM",
    "XOM", "LLY", "JNJ", "V", "PG", "MA", "AVGO", "HD", "CVX", "ORCL", "ABBV",
    "ADBE", "COST", "MRK", "PEP", "TMO", "KO", "WMT", "CSCO", "BAC", "MCD", "CRM",
    "ACN", "ABT", "LIN", "PFE", "AMD", "NFLX", "PM", "TXN", "INTC", "DIS", "INTU",
    "AMAT", "LOW", "UNP", "AMGN", "IBM", "CAT", "GE", "RTX", "BA", "GS", "SPGI",
    "COP", "ISRG", "PLD", "DE", "LMT", "BKNG", "AXP", "SYK", "T", "TJX", "MS", 
    "GILD", "LRCX", "VRTX", "AMT", "CVS", "MMC", "CI", "BMY", "REGN", "ADP", 
    "BLK", "CB", "MDT", "BSX", "SLB", "ZTS", "MU", "FI", "BDX", "PANW", "PGR", 
    "C", "SO", "MO", "EQIX", "ITW", "WM", "DUK", "VLO", "EOG", "HCA", "MPC", 
    "AON", "SNPS", "ICE", "MCK", "CME", "ORLY", "APH", "CL", "SHW", "KLAC", 
    "CDNS", "EMR", "NSC", "GD", "AIG", "PNC", "MAR", "HUM", "MCO", "ECL", "TGT", 
    "PSA", "USB", "ROP", "NXPI", "COF", "FDX", "EW", "PSX", "ADSK", "AJG", "D", 
    "PH", "CNC", "A", "MGM", "HLT", "O", "MET", "CARR", "SRE", "TRV", "AZO", 
    "F", "WELL", "MSI", "AEP", "ALL", "DLR", "IQV", "DXCM", "EFC", "PAYX", "TEL", 
    "DOW", "OXY", "HES", "STZ", "KMB", "GIS", "IDXX", "KDP", "DLTR", "SYY", 
    "VRSK", "BKR", "DHI", "GPN", "PRU", "EXC", "WBA", "LEN", "AFL", "EA", "NEM", 
    "OTIS", "PEG", "CPRT", "ROK", "CTAS", "ED", "BIIB", "BK", "CTVA", "XEL", 
    "RMD", "MNST", "HPQ", "KEYS", "VICI", "WDS", "GWW", "PCAR", "CDW", "FAST", 
    "TRGP", "VRSN", "KHC", "GEHC", "MTB", "MPWR", "FITB", "GLW", "WBD", "DFS", 
    "EFX", "EBAY", "AWK", "PPG", "LUV", "ON", "EIX", "ES", "DTE", "CSGP", "ROST", 
    "WTW", "BRO", "TSN", "HWM", "OKE", "EPAM", "VTR", "AVB", "CBRE", "ARE", 
    "DAL", "UAL", "WY", "FE", "EXPD", "ZBH", "WEC", "CHTR", "NVR", "XYL", "INVH"
]

@st.cache_data(ttl=3600)
def fetch_multitemporal_data():
    results = []
    with st.spinner("Calculando temporalidades (esto puede tardar 1 min)..."):
        # Descargamos 2 años para que el RSI Mensual sea preciso
        data = yf.download(tickers_sp500, period="2y", interval="1d", progress=False)['Close']
        
        for ticker in tickers_sp500:
            try:
                # --- DIARIO ---
                d_serie = data[ticker].dropna()
                if len(d_serie) < 14: continue
                rsi_d = ta.rsi(d_serie, length=14).iloc[-1]
                
                # --- SEMANAL ---
                w_serie = d_serie.resample('W').last()
                rsi_w = ta.rsi(w_serie, length=14).iloc[-1] if len(w_serie) > 14 else None
                
                # --- MENSUAL ---
                m_serie = d_serie.resample('M').last()
                rsi_m = ta.rsi(m_serie, length=14).iloc[-1] if len(m_serie) > 14 else None
                
                results.append({
                    "Ticket": ticker,
                    "Precio": round(float(d_serie.iloc[-1]), 2),
                    "RSI Diario": round(float(rsi_d), 2),
                    "RSI Semanal": round(float(rsi_w), 2) if rsi_w else "N/A",
                    "RSI Mensual": round(float(rsi_m), 2) if rsi_m else "N/A"
                })
            except: continue
    return pd.DataFrame(results)

# --- SIDEBAR ---
st.sidebar.header("Opciones de Radar")
temporalidad = st.sidebar.radio("Temporalidad Principal para Filtro:", ["Diario", "Semanal", "Mensual"])
filtro_tipo = st.sidebar.selectbox("Estado:", ["Todo", "🟢 Oportunidad (RSI < 35)", "🔥 Sobrecompra (RSI > 65)"])

if st.sidebar.button('🔄 Recargar Todo'):
    st.session_state.data_multi = fetch_multitemporal_data()

# --- LÓGICA ---
if 'data_multi' not in st.session_state:
    st.session_state.data_multi = fetch_multitemporal_data()

df = st.session_state.data_multi

if not df.empty:
    col_rsi = f"RSI {temporalidad}"
    
    # Aplicar Filtros
    if "Oportunidad" in filtro_tipo:
        df_final = df[df[col_rsi].apply(lambda x: x != "N/A" and x < 35)]
    elif "Sobrecompra" in filtro_tipo:
        df_final = df[df[col_rsi].apply(lambda x: x != "N/A" and x > 65)]
    else:
        df_final = df

    # Métricas
    m1, m2, m3 = st.columns(3)
    m1.metric(f"Activos en {temporalidad}", len(df_final))
    m2.metric("Oportunidades (D)", len(df[df['RSI Diario'].apply(lambda x: x != "N/A" and x < 35)]))
    m3.metric("Oportunidades (W)", len(df[df['RSI Semanal'].apply(lambda x: x != "N/A" and x < 35)]))

    st.divider()
    # Formatear tabla con colores
    def color_rsi(val):
        if val == "N/A": return ""
        color = 'background-color: #d4edda' if val < 35 else ('background-color: #f8d7da' if val > 65 else '')
        return color

    st.dataframe(df_final.style.applymap(color_rsi, subset=['RSI Diario', 'RSI Semanal', 'RSI Mensual']), use_container_width=True)
else:
    st.info("Cargando datos del mercado...")
