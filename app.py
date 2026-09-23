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

LOGO_PATH = "assets/agromar_logo.png"

st.set_page_config(page_title="Mantenimiento TASTE", page_icon=LOGO_PATH, layout="wide")
ui_style.inject()


# ============================ ACCESO ============================
def verificar_acceso() -> bool:
    clave_correcta = st.secrets.get("APP_PASSWORD")
    if not clave_correcta:
        return True
    if st.session_state.get("autenticado"):
        return True

    # Fondo decorativo difuminado (patrón industrial sutil, no una foto real
    # todavía). Si tienes una foto propia del TASTE, pásame su URL y la
    # reemplazo aquí como imagen de fondo real, atenuada con el mismo filtro.
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 15% 20%, rgba(245,130,30,0.10), transparent 45%),
                radial-gradient(circle at 85% 75%, rgba(60,139,60,0.10), transparent 45%),
                var(--background-color);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    _, col_centro, _ = st.columns([1, 1.1, 1])
    with col_centro:
        st.write("")
        st.write("")
        st.image(LOGO_PATH, width=160)
        with st.container(border=True):
            st.markdown("#### Mantenimiento TASTE")
            st.caption("Agromar Industrial S.A. · Planta Huacho — Acceso restringido")
            clave = st.text_input("Clave de acceso", type="password", label_visibility="collapsed",
                                   placeholder="Ingresa la clave de acceso")
            if st.button("Entrar", use_container_width=True):
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
    c_logo, c_nombre = st.columns([1, 2.2])
    with c_logo:
        st.image(LOGO_PATH, width=48)
    with c_nombre:
        st.markdown("<div style='font-size:1.15rem;font-weight:700;padding-top:6px;'>TASTE</div>",
                     unsafe_allow_html=True)
    st.caption("Agromar Industrial S.A. · Planta Huacho")
    st.write("")

    pagina = option_menu(
        menu_title=None,
        options=PAGINAS,
        icons=ICONOS,
        default_index=0,
        styles={
            "container": {"padding": "0", "background-color": "transparent"},
            "icon": {"color": "var(--primary-color)", "font-size": "15px"},
            "nav-link": {
                "font-size": "14.5px",
                "text-align": "left",
                "margin": "3px 0",
                "border-radius": "10px",
                "color": "var(--text-color)",
                "padding": "10px 12px",
            },
            "nav-link-selected": {
                "background-color": "var(--secondary-background-color)",
                "color": "var(--primary-color)",
            },
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
