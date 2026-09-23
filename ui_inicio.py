"""
ui_inicio.py - Portada: ficha técnica del Evaporador TASTE.
Datos tomados de los planos DWG N.º 1-903 (JOB #1178) y de la hoja de
requerimientos de servicios (utilities) compartida.
"""
import streamlit as st
from db import listar


def _spec_card(columna, etiqueta: str, valor: str):
    columna.markdown(
        f"""
        <div class="spec-card">
            <div class="etiqueta">{etiqueta}</div>
            <div class="valor">{valor}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render():
    equipos = listar("equipos")
    nombre_equipo = equipos[0]["nombre"] if equipos else "Evaporador TASTE"
    ubicacion = equipos[0].get("ubicacion") if equipos else None

    st.markdown(
        f"""
        <div class="hero">
            <h1>{nombre_equipo}</h1>
            <p>Evaporador de 6 etapas (T.A.S.T.E.) · {ubicacion or 'Ficha técnica y requerimientos de servicios industriales'}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Requerimientos de servicios (utilities)")
    c1, c2, c3 = st.columns(3)
    _spec_card(c1, "Vapor", "3 000 kg/h (6 650 lb/h) · mín. 9 bar")
    _spec_card(c2, "Tasa de evaporación", "27 000 lb/h")
    _spec_card(c3, "Aire comprimido seco", "0.85 m³/min (3 cfm) · mín. 5 bar")

    c4, c5, c6 = st.columns(3)
    _spec_card(c4, "Agua potable (sellos de bombas)", "8 L/min")
    _spec_card(c5, "Agua de refrigeración", "2 200 L/min (585 gpm) @ 29 °C")
    _spec_card(c6, "Requerimiento eléctrico", "440 V CA · 3F · 60 Hz · 125 A · 57 kW")

    st.caption("El requerimiento de vapor incluye el enfriador instantáneo (flash cooler).")

    st.markdown("#### Conexiones principales")
    st.caption("Según plano de layout, DWG N.º 1-903")
    st.table(
        {
            "Conexión": [
                "Producto — Salida",
                "Alimentación — Entrada",
                "Vapor — Entrada",
                "Agua de refrigeración — Entrada",
                "Condensado de producto — Salida",
                "Condensado de vapor — Salida",
            ],
            "Diámetro": ["2\" OD", "2\" OD", "4.5\" OD", "4.5\" OD", "1.9\" OD", "1.9\" OD"],
        }
    )

    col_izq, col_der = st.columns(2)
    with col_izq:
        st.markdown("#### Bomba de producto (referencia de plano)")
        st.markdown("- **Modelo**: Waukesha 130U2\n- **Motor**: 7.5 HP / 1800 RPM")
    with col_der:
        st.markdown("#### Documentación disponible")
        st.markdown(
            "- DWG N.º 1-903 — Isométrico de tuberías (JOB #1178)\n"
            "- DWG N.º 1-903 — Layout general y conexiones\n"
            "- DWG N.º 1-903 — Base de concreto y anclajes"
        )

    st.caption(
        "Cotas generales de layout, especificaciones de la base de concreto (profundidad mínima "
        "36\", concreto de 27 MPa) y detalle de anclajes disponibles en los planos originales."
    )
