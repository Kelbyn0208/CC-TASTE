"""
ui_mantenimiento.py - Registro y gestión de intervenciones de mantenimiento.
"""
import streamlit as st
import pandas as pd
from datetime import date
from db import listar, crear, eliminar, historial_intervenciones


def registrar_intervencion():
    st.markdown("#### Nueva intervención")
    equipos = listar("equipos")
    if not equipos:
        st.info("Primero crea el equipo en la pestaña Jerarquía.")
        return
    equipo_id = equipos[0]["id"]  # se asume un solo equipo (TASTE)

    etapas = listar("etapas", filtros={"equipo_id": equipo_id}, orden="orden")
    if not etapas:
        st.info("Este equipo no tiene etapas registradas.")
        return
    etapa_id = st.selectbox("Etapa", [e["id"] for e in etapas],
                             format_func=lambda eid: next(e["nombre"] for e in etapas if e["id"] == eid))

    area_id = st.selectbox("Área", ["Mecánica", "Eléctrica", "Neumática", "Electrónica"])

    componentes = listar("componentes", filtros={"etapa_id": etapa_id, "area": area_id}, orden="nombre")
    if not componentes:
        st.warning("Esta etapa no tiene componentes registrados en esa área.")
        return
    componente_id = st.selectbox("Componente", [c["id"] for c in componentes],
                                  format_func=lambda cid: next(c["nombre"] for c in componentes if c["id"] == cid))

    repuestos = listar("repuestos", filtros={"componente_id": componente_id}, orden="nombre")
    if not repuestos:
        st.warning("Este componente no tiene repuestos registrados.")
        return

    with st.form("form_intervencion", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("Fecha", value=date.today())
            repuesto_id = st.selectbox("Repuesto utilizado", [r["id"] for r in repuestos],
                                        format_func=lambda rid: next(r["nombre"] for r in repuestos if r["id"] == rid))
            cantidad = st.number_input("Cantidad", min_value=0.01, value=1.0, step=1.0)
        with col2:
            tipo = st.selectbox("Tipo", ["Preventivo", "Correctivo"])
            horas_parada = st.number_input("Horas de parada", min_value=0.0, value=0.0, step=0.5)
            tecnico = st.text_input("Técnico")
        observaciones = st.text_area("Observaciones")
        enviado = st.form_submit_button("Guardar intervención")

    if enviado:
        intervencion = crear("intervenciones", {
            "fecha": fecha.isoformat(), "etapa_id": etapa_id, "componente_id": componente_id,
            "tipo": tipo, "descripcion": observaciones, "horas_parada": horas_parada,
        })[0]

        crear("intervencion_repuestos", {
            "intervencion_id": intervencion["id"], "repuesto_id": repuesto_id, "cantidad": cantidad,
        })

        crear("kardex_movimientos", {
            "repuesto_id": repuesto_id, "tipo_movimiento": "SALIDA", "cantidad": cantidad,
            "fecha": fecha.isoformat(), "motivo": "Uso en mantenimiento",
            "intervencion_id": intervencion["id"], "usuario": tecnico,
        })
        st.success("Intervención registrada y descontada del stock.")
        st.rerun()


def listar_intervenciones():
    st.markdown("#### Intervenciones registradas")
    datos = historial_intervenciones()
    if not datos:
        st.info("Sin intervenciones todavía.")
        return

    filas = []
    for d in datos:
        etapa = (d.get("etapas") or {}).get("nombre")
        componente = (d.get("componentes") or {}).get("nombre")
        filas.append({"id": d["id"], "Fecha": d["fecha"], "Etapa": etapa, "Componente": componente,
                      "Tipo": d["tipo"], "Observaciones": d.get("descripcion")})
    df = pd.DataFrame(filas)
    st.dataframe(df.drop(columns=["id"]), use_container_width=True, hide_index=True)

    etiquetas = {f"{f['Fecha']} · {f['Etapa']} · {f['Componente']}": f["id"] for f in filas}
    sel = st.selectbox("Selecciona una intervención para eliminar", list(etiquetas.keys()))
    if st.button("Eliminar intervención seleccionada"):
        eliminar("intervenciones", etiquetas[sel])
        st.warning("Intervención eliminada. El stock del repuesto usado NO se revierte "
                    "(el repuesto ya salió físicamente); si fue un error, corrígelo desde Kardex.")
        st.rerun()


def render():
    st.header("Registro de Mantenimiento")
    sub = st.tabs(["Nueva intervención", "Ver / eliminar"])
    with sub[0]:
        registrar_intervencion()
    with sub[1]:
        listar_intervenciones()
