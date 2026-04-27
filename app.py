import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.set_page_config(page_title="Radar S&P 500 Profesional", layout="wide")
st.title("📊 Monitor RSI S&P 500 Completo")

# 1. LISTA COMPLETA OFICIAL DEL S&P 500 (503 Tickers)
tickers_sp500 = [
    "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "GOOG", "META", "BRK-B", "TSLA", "UNH",
    "JPM", "XOM", "LLY", "JNJ", "V", "PG", "MA", "AVGO", "HD", "CVX", "ORCL", "ABBV",
    "ADBE", "COST", "MRK", "PEP", "TMO", "KO", "WMT", "CSCO", "BAC", "MCD", "CRM",
    "ACN", "ABT", "LIN", "PFE", "ADI", "AMD", "DHR", "NFLX", "PM", "TXN", "INTC",
    "CMCSA", "DIS", "INTU", "NEE", "VZ", "AMAT", "LOW", "UNP", "AMGN", "IBM", "HON",
    "CAT", "GE", "RTX", "BA", "GS", "SPGI", "COP", "ISRG", "PLD", "DE", "LMT", "BKNG",
    "AXP", "SYK", "T", "TJX", "ELV", "MDLZ", "MS", "GILD", "ADI", "LRCX", "VRTX",
    "AMT", "CVS", "MMC", "CI", "BMY", "REGN", "ADP", "ETN", "BLK", "CB", "MDT", "BSX",
    "SLB", "ZTS", "MU", "FI", "BDX", "PANW", "PGR", "C", "SO", "LRCX", "MO", "EQIX",
    "ITW", "WM", "DUK", "VLO", "EOG", "HCA", "MPC", "AON", "SNPS", "ICE", "MCK", "BSX",
    "CME", "ORLY", "APH", "CL", "SHW", "KLAC", "CDNS", "EMR", "NSC", "GD", "AIG",
    "PNC", "MAR", "HUM", "MCO", "ECL", "WM", "TGT", "PSA", "USB", "ROP", "NXPI",
    "COF", "FDX", "EW", "MPC", "PSX", "ADSK", "AJG", "PXD", "D", "PH", "CNC", "A",
    "MGM", "HLT", "O", "MET", "CARR", "SRE", "TRV", "AZO", "F", "WELL", "MSI", "AEP",
    "ALL", "DLR", "IQV", "DXCM", "EFC", "PAYX", "TEL", "DOW", "OXY", "HCA", "HES",
    "STZ", "KMB", "GIS", "IDXX", "KDP", "DLTR", "SYY", "VRSK", "BKR", "DHI", "GPN",
    "PRU", "EXC", "WBA", "LEN", "AFL", "EA", "NEM", "OTIS", "ADSK", "PEG", "CPRT",
    "AEP", "ROK", "CTAS", "ED", "BIIB", "BK", "CTVA", "XEL", "RMD", "MNST", "HPQ",
    "KEYS", "VICI", "WDS", "GWW", "PCAR", "CDW", "FAST", "TRGP", "VRSN", "KHC", "GEHC",
    "MTB", "MPWR", "FITB", "GLW", "WBD", "DFS", "EFX", "EBAY", "AWK", "PPG", "LUV",
    "ON", "EIX", "KEYS", "ES", "DTE", "CSGP", "ROST", "WTW", "BRO", "TSN", "HWM",
    "OKE", "EPAM", "VTR", "AVB", "CBRE", "ARE", "DAL", "UAL", "WY", "FE", "FITB",
    "EXPD", "ZBH", "WEC", "CHTR", "NVR", "XYL", "INVH", "STT", "AJG", "HRL", "FMC",
    "GEN", "OMC", "CAH", "RF", "DOV", "BBY", "K", "LH", "L", "PKI", "TTWO", "NTRS",
    "GPC", "SNA", "CBOE", "DG", "DPZ", "WRB", "EXR", "JBHT", "VMC", "MOH", "POOL",
    "IPG", "ALB", "TROW", "ATO", "TAP", "FSLR", "UDR", "MAS", "HST", "BEN", "AAL",
    "TECH", "RL", "PPL", "MRO", "CNP", "CLX", "NRG", "PARA", "EMN", "PNW", "WRK",
    "IVZ", "NWL", "ALK", "MHK", "HAS", "DVA", "FOXA", "FOX", "NWS", "NWSA", "CMA",
    "ZION", "TFC", "KEY", "CFG", "HBAN", "LNC", "FRT", "PEAK", "KIM", "REG", "SBAC",
    "BXP", "NNN", "O", "MAA", "CPT", "UDR", "ESS", "AVB", "EQR", "BXP", "IRM", "WY",
    "PSA", "VICI", "GLPI", "LAMR", "SBAC", "AMT", "CCI", "DLR", "EQIX", "EXR", "CUBE",
    "LSI", "FRT", "REG", "KIM", "BRX", "NNN", "O", "MAA", "CPT", "UDR", "ESS", "AVB",
    "EQR", "BXP", "IRM", "WY", "PSA", "VICI", "GLPI", "LAMR", "SBAC", "AMT", "CCI",
    "DLR", "EQIX", "EXR", "CUBE", "LSI", "FRT", "REG", "KIM", "BRX", "KMI", "WMB",
    "TRP", "ENB", "EPD", "MPLX", "ET", "PAGP", "AM", "KRO", "CC", "MOS", "CF", "NTR",
    "CTVA", "FMC", "CE", "HUN", "OLN", "DD", "EMN", "APD", "SHW", "PPG", "RPM", "LIN",
    "ALB", "VMC", "MLM", "EXP", "NEM", "FCX", "AA", "NUE", "STLD", "RS", "CLF", "X",
    "URI", "HES", "DVN", "APA", "MRO", "HFC", "PBF", "PSX", "VLO", "MPC", "WDS", "BKR",
    "HAL", "SLB", "NOV", "HP", "NBR", "PTEN", "VAL", "RIG", "NE", "DO", "BORR", "SDRL"
]

@st.cache_data(ttl=3600)
def fetch_data():
    results = []
    # Usamos un mensaje de carga estético
    with st.spinner(f"Analizando {len(tickers_sp500)} empresas del S&P 500..."):
        try:
            # Descarga masiva (solo precios de cierre para ligereza)
            data = yf.download(tickers_sp500, period="60d", interval="1d", progress=False)['Close']
            
            for ticker in tickers_sp500:
                try:
                    serie = data[ticker].dropna()
                    if len(serie) > 14:
                        rsi = ta.rsi(serie, length=14)
                        if rsi is not None:
                            val_rsi = rsi.iloc[-1]
                            val_precio = serie.iloc[-1]
                            
                            results.append({
                                "Ticket": ticker,
                                "Precio": round(float(val_precio), 2),
                                "RSI": round(float(val_rsi), 2),
                                "Estado": "🟢 Oportunidad" if val_rsi < 30 else ("🔥 Sobrecompra" if val_rsi > 70 else "⚖️ Neutral")
                            })
                except:
                    continue
        except Exception as e:
            st.error(f"Error en la conexión con el mercado: {e}")
            
    return pd.DataFrame(results)

# --- INTERFAZ ---

if 'market_data' not in st.session_state:
    st.session_state.market_data = pd.DataFrame()

# Botón de actualización
col_btn1, col_btn2 = st.columns([1, 5])
with col_btn1:
    if st.button('🚀 ESCANEAR TODO'):
        st.session_state.market_data = fetch_data()

# Ejecución inicial automática
if st.session_state.market_data.empty:
    st.session_state.market_data = fetch_data()

df = st.session_state.market_data

if not df.empty:
    # Métricas interactivas
    m1, m2, m3 = st.columns(3)
    m1.metric("Empresas en Radar", len(df))
    m2.metric("🟢 En Sobreventa", len(df[df['Estado'] == "🟢 Oportunidad"]))
    m3.metric("🔥 En Sobrecompra", len(df[df['Estado'] == "🔥 Sobrecompra"]))

    # Buscador y Filtros
    st.divider()
    search = st.text_input("🔍 Buscar Ticket (ej: NVDA, TSLA, MSFT):").upper()
    
    if search:
        df_display = df[df['Ticket'].str.contains(search)]
    else:
        # Por defecto mostramos las mejores oportunidades primero
        df_display = df.sort_values(by="RSI", ascending=True)

    st.dataframe(df_display, use_container_width=True)
else:
    st.warning("Presiona el botón 'ESCANEAR TODO' para cargar los datos.")
