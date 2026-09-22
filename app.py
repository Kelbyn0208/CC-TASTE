"""
app.py - Sistema de Mantenimiento y Kardex del Evaporador TASTE.
Navegación por barra lateral; la lógica vive en db.py y en los módulos ui_*.py.
"""
import streamlit as st
import ui_jerarquia
import ui_kardex
import ui_mantenimiento
import ui_despiece
import ui_reportes
from db import listar, repuestos_para_reponer

st.set_page_config(page_title="Mantenimiento TASTE", page_icon="🛠️", layout="wide")


# ============================ ACCESO ============================
def verificar_acceso():
    clave_correcta = st.secrets.get("APP_PASSWORD")
    if not clave_correcta:
        return True
    if st.session_state.get("autenticado"):
        return True

    st.title("🛠️ Mantenimiento TASTE")
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
PAGINAS = ["🏗️ Jerarquía", "📦 Kardex", "🔧 Mantenimiento", "🖼️ Despiece", "📊 Reportes"]

with st.sidebar:
    st.markdown("## 🛠️ TASTE")
    st.caption("Agromar Industrial S.A. · Planta Huacho")
    st.divider()
    pagina = st.radio("Navegación", PAGINAS, label_visibility="collapsed")
    st.divider()
    st.metric("Repuestos registrados", len(listar("repuestos")))
    st.metric("⚠️ Alertas de reposición", len(repuestos_para_reponer()))


# ============================ ENCABEZADO ============================
st.title("Sistema de Mantenimiento y Kardex - Evaporador TASTE")

col1, col2, col3 = st.columns(3)
col1.metric("Etapas", len(listar("etapas")))
col2.metric("Componentes", len(listar("componentes")))
col3.metric("Repuestos", len(listar("repuestos")))
st.divider()


# ============================ CONTENIDO ============================
if pagina == "🏗️ Jerarquía":
    ui_jerarquia.render()
elif pagina == "📦 Kardex":
    ui_kardex.render()
elif pagina == "🔧 Mantenimiento":
    ui_mantenimiento.render()
elif pagina == "🖼️ Despiece":
    ui_despiece.render()
elif pagina == "📊 Reportes":
    ui_reportes.render()
