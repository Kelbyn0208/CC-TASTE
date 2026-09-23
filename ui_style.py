"""
ui_style.py - Estilos globales inyectados una sola vez desde app.py.

IMPORTANTE: los colores usan las variables de tema que Streamlit expone
(--primary-color, --background-color, --secondary-background-color,
--text-color). Así, si el visitante cambia entre modo claro/oscuro desde
el menú de Streamlit, la interfaz se adapta automáticamente en vez de
quedar con colores fijos pensados solo para modo oscuro.
"""
import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif;
}

:root {
    --taste-primary: var(--primary-color, #F5821E);
    --taste-green: #3C8B3C;
    --taste-bg2: var(--secondary-background-color, #1E293B);
    --taste-border: rgba(128, 128, 128, 0.25);
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
    background: var(--taste-bg2);
    border: 1px solid var(--taste-border);
    padding: 1rem 1.2rem;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.12);
}
[data-testid="stMetricLabel"] { opacity: 0.7; font-weight: 500; }
[data-testid="stMetricValue"] { color: var(--taste-primary) !important; }

/* Formularios */
div[data-testid="stForm"] {
    background: var(--taste-bg2);
    border: 1px solid var(--taste-border);
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
    border: 1px solid var(--taste-border);
}

/* Portada */
.hero {
    background: var(--taste-bg2);
    border: 1px solid var(--taste-border);
    border-top: 4px solid var(--taste-primary);
    border-radius: 16px;
    padding: 2.4rem 2.6rem;
    margin-bottom: 1.8rem;
}
.hero h1 { margin: 0; font-size: 2.1rem; }
.hero p { opacity: 0.7; margin-top: 0.5rem; font-size: 1.02rem; }

.spec-card {
    background: var(--taste-bg2);
    border: 1px solid var(--taste-border);
    border-radius: 14px;
    padding: 1.15rem 1.3rem;
    height: 100%;
    margin-bottom: 0.9rem;
}
.spec-card .etiqueta {
    opacity: 0.65;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
}
.spec-card .valor {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--taste-primary);
    margin-top: 0.2rem;
}

hr { border-color: var(--taste-border) !important; }
</style>
"""


def inject():
    st.markdown(CSS, unsafe_allow_html=True)
