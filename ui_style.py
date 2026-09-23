"""
ui_style.py - Estilos globales inyectados una sola vez desde app.py.
"""
import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif;
}

.main .block-container {
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

h1, h2, h3 {
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}

/* Tarjetas de métricas nativas de Streamlit */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #1E293B, #141a26);
    border: 1px solid #2a3548;
    padding: 1rem 1.2rem;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
}
[data-testid="stMetricLabel"] { color: #94A3B8 !important; font-weight: 500; }
[data-testid="stMetricValue"] { color: #F2A93B !important; }

/* Formularios */
div[data-testid="stForm"] {
    background: #141a26;
    border: 1px solid #232c3d;
    border-radius: 16px;
    padding: 1.5rem 1.7rem;
}

/* Botones */
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* Tablas y dataframes */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #232c3d;
}

/* Portada */
.hero {
    background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
    border: 1px solid #2a3548;
    border-radius: 20px;
    padding: 2.4rem 2.6rem;
    margin-bottom: 1.8rem;
}
.hero h1 { margin: 0; font-size: 2.1rem; color: #F8FAFC; }
.hero p { color: #94A3B8; margin-top: 0.5rem; font-size: 1.02rem; }

.spec-card {
    background: #141a26;
    border: 1px solid #232c3d;
    border-radius: 14px;
    padding: 1.15rem 1.3rem;
    height: 100%;
    margin-bottom: 0.9rem;
}
.spec-card .etiqueta {
    color: #94A3B8;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
}
.spec-card .valor {
    font-size: 1.25rem;
    font-weight: 700;
    color: #F2A93B;
    margin-top: 0.2rem;
}

hr { border-color: #232c3d !important; }
</style>
"""


def inject():
    st.markdown(CSS, unsafe_allow_html=True)
