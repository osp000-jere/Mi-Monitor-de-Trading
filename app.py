import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.set_page_config(page_title="Radar S&P 500 Profesional", layout="wide")
st.title("📊 Monitor RSI S&P 500 Personalizado")

# Lista de activos (500 principales)
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
    "COF", "FDX", "EW", "PSX", "ADSK", "AJG", "D", "PH", "CNC", "A",
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

# --- CONFIGURACIÓN DE PARÁMETROS ---
st.sidebar.header("⚙️ Configuración")

temp_choice = st.sidebar.selectbox(
    "1. Selecciona Temporalidad:",
    ["Diario", "Semanal", "Mensual"]
)

filtro_estado = st.sidebar.radio(
    "2. Filtrar por:",
    ["Oportunidades (RSI < 30)", "Sobrecompras (RSI > 70)", "Ver Todo"]
)

def fetch_data_by_temp(temp):
    results = []
    # Definimos el periodo según la temporalidad para optimizar carga
    # Mensual necesita al menos 2 años de datos diarios para calcular 14 meses
    periodo = "2y" if temp in ["Semanal", "Mensual"] else "60d"
    
    with st.spinner(f"Escaneando mercado en formato {temp}..."):
        try:
            data = yf.download(tickers_sp500, period=periodo, interval="1d", progress=False)['Close']
            
            for ticker in tickers_sp500:
                try:
                    d_serie = data[ticker].dropna()
                    
                    # Convertimos la temporalidad si es necesario
                    if temp == "Semanal":
                        serie = d_serie.resample('W').last()
                    elif temp == "Mensual":
                        serie = d_serie.resample('M').last()
                    else:
                        serie = d_serie
                    
                    if len(serie) > 14:
                        rsi_val = ta.rsi(serie, length=14).iloc[-1]
                        results.append({
                            "Ticket": ticker,
                            "Precio": round(float(d_serie.iloc[-1]), 2),
                            "RSI": round(float(rsi_val), 2),
                            "Temporalidad": temp
                        })
                except: continue
        except Exception as e:
            st.error(f"Error de conexión: {e}")
            
    return pd.DataFrame(results)

# --- BOTÓN DE EJECUCIÓN ---
if st.sidebar.button('🚀 EJECUTAR ESCÁNER'):
    st.session_state.df_temp = fetch_data_by_temp(temp_choice)

# --- MOSTRAR RESULTADOS ---
if 'df_temp' in st.session_state and not st.session_state.df_temp.empty:
    df = st.session_state.df_temp
    
    # Aplicar filtros de estado
    if "Oportunidades" in filtro_estado:
        df_final = df[df['RSI'] < 30]
    elif "Sobrecompras" in filtro_estado:
        df_final = df[df['RSI'] > 70]
    else:
        df_final = df

    # Métricas
    m1, m2 = st.columns(2)
    m1.metric(f"Activos en {temp_choice}", len(df_final))
    m2.metric("RSI Promedio", round(df_final['RSI'].mean(), 2) if not df_final.empty else 0)

    st.divider()
    st.dataframe(df_final.sort_values(by="RSI"), use_container_width=True)
else:
    st.info("Selecciona los parámetros a la izquierda y presiona 'EJECUTAR ESCÁNER'.")
