"""
app.py - Sistema de Mantenimiento y Kardex del Evaporador TASTE.
Navegación por barra lateral con iconos; la lógica vive en db.py y en
los módulos ui_*.py.
"""
import streamlit as st
from streamlit_option_menu import option_menu

import ui_style
import ui_inicio
import ui_jerarquia
import ui_kardex
import ui_mantenimiento
import ui_despiece
import ui_reportes
from db import listar, repuestos_para_reponer

st.set_page_config(page_title="Mantenimiento TASTE", page_icon="⚙️", layout="wide")
ui_style.inject()


# ============================ ACCESO ============================
def verificar_acceso() -> bool:
    clave_correcta = st.secrets.get("APP_PASSWORD")
    if not clave_correcta:
        return True
    if st.session_state.get("autenticado"):
        return True

    st.markdown("<div class='hero'><h1>Mantenimiento TASTE</h1></div>", unsafe_allow_html=True)
    clave = st.text_input("Ingresa la clave de acceso", type="password")
    if st.button("Entrar"):
        if clave == clave_correcta:
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Clave incorrecta.")
    return False


if not verificar_acceso():
    st.stop()


# ============================ BARRA LATERAL ============================
PAGINAS = ["Inicio", "Jerarquía", "Kardex", "Mantenimiento", "Despiece", "Reportes"]
ICONOS = ["house", "diagram-3", "box-seam", "tools", "puzzle", "bar-chart-line"]

with st.sidebar:
    st.markdown(
        "<div style='display:flex;align-items:center;gap:10px;margin-bottom:2px;'>"
        "<span style='font-size:1.5rem;'>⚙️</span>"
        "<span style='font-size:1.3rem;font-weight:700;'>TASTE</span></div>",
        unsafe_allow_html=True,
    )
    st.caption("Agromar Industrial S.A. · Planta Huacho")
    st.write("")

    pagina = option_menu(
        menu_title=None,
        options=PAGINAS,
        icons=ICONOS,
        default_index=0,
        styles={
            "container": {"padding": "0", "background-color": "transparent"},
            "icon": {"color": "#F2A93B", "font-size": "15px"},
            "nav-link": {
                "font-size": "14.5px",
                "text-align": "left",
                "margin": "3px 0",
                "border-radius": "10px",
                "color": "#E2E8F0",
                "padding": "10px 12px",
            },
            "nav-link-selected": {"background-color": "#1E293B", "color": "#F2A93B"},
        },
    )

    st.divider()
    st.metric("Repuestos registrados", len(listar("repuestos")))
    st.metric("Alertas de reposición", len(repuestos_para_reponer()))


# ============================ CONTENIDO ============================
if pagina == "Inicio":
    ui_inicio.render()
else:
    st.title("Sistema de Mantenimiento y Kardex")
    c1, c2, c3 = st.columns(3)
    c1.metric("Etapas", len(listar("etapas")))
    c2.metric("Componentes", len(listar("componentes")))
    c3.metric("Repuestos", len(listar("repuestos")))
    st.divider()

    if pagina == "Jerarquía":
        ui_jerarquia.render()
    elif pagina == "Kardex":
        ui_kardex.render()
    elif pagina == "Mantenimiento":
        ui_mantenimiento.render()
    elif pagina == "Despiece":
        ui_despiece.render()
    elif pagina == "Reportes":
        ui_reportes.render()
