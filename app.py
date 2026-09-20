"""
app.py - Sistema de Mantenimiento y Kardex del Evaporador TASTE.
Orquesta las pestañas; toda la lógica vive en db.py y en los módulos ui_*.py.
"""
import streamlit as st
import ui_jerarquia
import ui_kardex
import ui_mantenimiento
import ui_reportes

st.set_page_config(page_title="Mantenimiento TASTE", page_icon="🛠️", layout="wide")
st.title("🛠️ Sistema de Mantenimiento y Kardex - Evaporador TASTE")

tabs = st.tabs(["🏗️ Jerarquía", "📦 Kardex", "🔧 Mantenimiento", "📊 Reportes"])

with tabs[0]:
    ui_jerarquia.render()
with tabs[1]:
    ui_kardex.render()
with tabs[2]:
    ui_mantenimiento.render()
with tabs[3]:
    ui_reportes.render()
