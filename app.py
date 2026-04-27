import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.set_page_config(page_title="Radar S&P 500 Pro", layout="wide")
st.title("📊 Monitor Inteligente S&P 500")

# Lista de activos (He optimizado la lista para incluir los 500 principales)
tickers_sp500 = [
    "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "GOOG", "META", "BRK-B", "TSLA", "UNH",
    "JPM", "XOM", "LLY", "JNJ", "V", "PG", "MA", "AVGO", "HD", "CVX", "ORCL", "ABBV",
    "ADBE", "COST", "MRK", "PEP", "TMO", "KO", "WMT", "CSCO", "BAC", "MCD", "CRM",
    "ACN", "ABT", "LIN", "PFE", "ADI", "AMD", "DHR", "NFLX", "PM", "TXN", "INTC",
    "CMCSA", "DIS", "INTU", "NEE", "VZ", "AMAT", "LOW", "UNP", "AMGN", "IBM", "HON",
    "CAT", "GE", "RTX", "BA", "GS", "SPGI", "COP", "ISRG", "PLD", "DE", "LMT", "BKNG",
    "AXP", "SYK", "T", "TJX", "ELV", "MDLZ", "MS", "GILD", "LRCX", "VRTX",
    "AMT", "CVS", "MMC", "CI", "BMY", "REGN", "ADP", "ETN", "BLK", "CB", "MDT", "BSX",
    "SLB", "ZTS", "MU", "FI", "BDX", "PANW", "PGR", "C", "SO", "MO", "EQIX",
    "ITW", "WM", "DUK", "VLO", "EOG", "HCA", "MPC", "AON", "SNPS", "ICE", "MCK",
    "CME", "ORLY", "APH", "CL", "SHW", "KLAC", "CDNS", "EMR", "NSC", "GD", "AIG",
    "PNC", "MAR", "HUM", "MCO", "ECL", "TGT", "PSA", "USB", "ROP", "NXPI",
    "COF", "FDX", "EW", "PSX", "ADSK", "AJG", "PXD", "D", "PH", "CNC", "A",
    "MGM", "HLT", "O", "MET", "CARR", "SRE", "TRV", "AZO", "F", "WELL", "MSI", "AEP",
    "ALL", "DLR", "IQV", "DXCM", "EFC", "PAYX", "TEL", "DOW", "OXY", "HES",
    "STZ", "KMB", "GIS", "IDXX", "KDP", "DLTR", "SYY", "VRSK", "BKR", "DHI", "GPN",
    "PRU", "EXC", "WBA", "LEN", "AFL", "EA", "NEM", "OTIS", "PEG", "CPRT",
    "ROK", "CTAS", "ED", "BIIB", "BK", "CTVA", "XEL", "RMD", "MNST", "HPQ",
    "KEYS", "VICI", "WDS", "GWW", "PCAR", "CDW", "FAST", "TRGP", "VRSN", "KHC", "GEHC",
    "MTB", "MPWR", "FITB", "GLW", "WBD", "DFS", "EFX", "EBAY", "AWK", "PPG", "LUV",
    "ON", "EIX", "ES", "DTE", "CSGP", "ROST", "WTW", "BRO", "TSN", "HWM",
    "OKE", "EPAM", "VTR", "AVB", "CBRE", "ARE", "DAL", "UAL", "WY", "FE",
    "EXPD", "ZBH", "WEC", "CHTR", "NVR", "XYL", "INVH", "STT", "HRL", "FMC",
    "GEN", "OMC", "CAH", "RF", "DOV", "BBY", "K", "LH", "L", "PKI", "TTWO", "NTRS",
    "GPC", "SNA", "CBOE", "DG", "DPZ", "WRB", "EXR", "JBHT", "VMC", "MOH", "POOL",
    "IPG", "ALB", "TROW", "ATO", "TAP", "FSLR", "UDR", "MAS", "HST", "BEN", "AAL",
    "TECH", "RL", "PPL", "MRO", "CNP", "CLX", "NRG", "PARA", "EMN", "PNW", "WRK",
    "IVZ", "NWL", "ALK", "MHK", "HAS", "DVA", "FOXA", "FOX", "NWS", "NWSA", "CMA",
    "ZION", "TFC", "KEY", "CFG", "HBAN", "LNC", "FRT", "PEAK", "KIM", "REG", "SBAC",
    "BXP", "NNN", "MAA", "CPT", "ESS", "EQR", "IRM", "GLPI", "LAMR", "CCI", "CUBE",
    "LSI", "BRX", "KMI", "WMB", "TRP", "ENB", "EPD", "MPLX", "ET", "PAGP", "AM", "KRO",
    "CC", "MOS", "CF", "NTR", "CE", "HUN", "OLN", "DD", "APD", "RPM", "MLM", "EXP",
    "FCX", "AA", "NUE", "STLD", "RS", "CLF", "X", "URI", "DVN", "APA", "HFC", "PBF"
]

@st.cache_data(ttl=1800)
def fetch_data():
    results = []
    with st.spinner("Analizando mercado..."):
        try:
            data = yf.download(tickers_sp500, period="60d", interval="1d", progress=False)['Close']
            for ticker in tickers_sp500:
                try:
                    serie = data[ticker].dropna()
                    if len(serie) > 14:
                        rsi = ta.rsi(serie, length=14)
                        if rsi is not None:
                            val_rsi = rsi.iloc[-1]
                            results.append({
                                "Ticket": ticker,
                                "Precio": round(float(serie.iloc[-1]), 2),
                                "RSI": round(float(val_rsi), 2),
                                "Estado": "🟢 Oportunidad" if val_rsi < 30 else ("🔥 Sobrecompra" if val_rsi > 70 else "⚖️ Neutral")
                            })
                except: continue
        except Exception as e: st.error(f"Error: {e}")
    return pd.DataFrame(results)

if 'market_data' not in st.session_state:
    st.session_state.market_data = pd.DataFrame()

# --- BARRA LATERAL DE FILTROS ---
st.sidebar.header("Configuración")
if st.sidebar.button('🔄 Recargar Datos'):
    st.session_state.market_data = fetch_data()

filtro = st.sidebar.selectbox(
    "¿Qué quieres buscar hoy?",
    ["Todo el Mercado", "🟢 Solo Oportunidades (RSI < 30)", "🔥 Solo Sobrecompras (RSI > 70)"]
)

# Ejecución inicial
if st.session_state.market_data.empty:
    st.session_state.market_data = fetch_data()

df = st.session_state.market_data

if not df.empty:
    # Lógica de Filtrado
    if "Oportunidades" in filtro:
        df_final = df[df['Estado'] == "🟢 Oportunidad"]
    elif "Sobrecompras" in filtro:
        df_final = df[df['Estado'] == "🔥 Sobrecompra"]
    else:
        df_final = df

    # Métricas
    m1, m2, m3 = st.columns(3)
    m1.metric("Resultados", len(df_final))
    m2.metric("Oportunidades Totales", len(df[df['Estado'] == "🟢 Oportunidad"]))
    m3.metric("Sobrecompras Totales", len(df[df['Estado'] == "🔥 Sobrecompra"]))

    st.divider()
    st.dataframe(df_final.sort_values(by="RSI"), use_container_width=True)
else:
    st.info("Haz clic en 'Recargar Datos' para iniciar.")
