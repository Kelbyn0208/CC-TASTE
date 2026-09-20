"""
ui_jerarquia.py - Gestión CRUD de Equipos, Etapas, Componentes y Repuestos.
"""
import streamlit as st
import pandas as pd
from db import listar, crear, actualizar, eliminar


def _selector_registro(registros: list[dict], etiqueta_campo: str, key: str):
    """Selectbox con la opción '➕ Nuevo' + los registros existentes.
    Devuelve (id_seleccionado_o_None, registro_actual_dict)."""
    opciones = {"➕ Nuevo": None}
    opciones.update({r[etiqueta_campo]: r["id"] for r in registros})
    seleccion = st.selectbox("Selecciona para editar (o crea uno nuevo)", list(opciones.keys()), key=key)
    id_sel = opciones[seleccion]
    actual = next((r for r in registros if r["id"] == id_sel), {})
    return id_sel, actual


def gestionar_equipos():
    st.markdown("#### Equipos")
    equipos = listar("equipos", orden="nombre")
    if equipos:
        st.dataframe(pd.DataFrame(equipos)[["nombre", "fabricante", "ubicacion"]],
                     use_container_width=True, hide_index=True)

    id_sel, actual = _selector_registro(equipos, "nombre", "sel_equipo")

    with st.form("form_equipo"):
        nombre = st.text_input("Nombre*", value=actual.get("nombre", ""))
        fabricante = st.text_input("Fabricante", value=actual.get("fabricante", ""))
        ubicacion = st.text_input("Ubicación", value=actual.get("ubicacion", ""))
        descripcion = st.text_area("Descripción", value=actual.get("descripcion", ""))
        imagen_url = st.text_input("URL de imagen (Supabase Storage)", value=actual.get("imagen_url", ""))
        c1, c2 = st.columns(2)
        guardar = c1.form_submit_button("💾 Guardar")
        borrar = c2.form_submit_button("🗑️ Eliminar", disabled=(id_sel is None))

    data = {"nombre": nombre, "fabricante": fabricante, "ubicacion": ubicacion,
            "descripcion": descripcion, "imagen_url": imagen_url}

    if guardar and nombre:
        actualizar("equipos", id_sel, data) if id_sel else crear("equipos", data)
        st.success("Equipo guardado.")
        st.rerun()

    if borrar and id_sel:
        eliminar("equipos", id_sel)
        st.warning("Equipo eliminado (junto con todo lo que dependía de él).")
        st.rerun()


def gestionar_etapas():
    st.markdown("#### Etapas")
    equipos = listar("equipos", orden="nombre")
    if not equipos:
        st.info("Primero crea un equipo en la sub-pestaña anterior.")
        return

    equipo_id = st.selectbox("Equipo", [e["id"] for e in equipos],
                              format_func=lambda eid: next(e["nombre"] for e in equipos if e["id"] == eid),
                              key="equipo_para_etapas")

    etapas = listar("etapas", filtros={"equipo_id": equipo_id}, orden="orden")
    if etapas:
        st.dataframe(pd.DataFrame(etapas)[["nombre", "orden"]], use_container_width=True, hide_index=True)

    id_sel, actual = _selector_registro(etapas, "nombre", "sel_etapa")

    with st.form("form_etapa"):
        nombre = st.text_input("Nombre*", value=actual.get("nombre", ""))
        orden = st.number_input("Orden (1-6)", min_value=1, max_value=6, value=int(actual.get("orden", 1)))
        descripcion = st.text_area("Descripción", value=actual.get("descripcion", ""))
        imagen_url = st.text_input("URL de imagen", value=actual.get("imagen_url", ""))
        c1, c2 = st.columns(2)
        guardar = c1.form_submit_button("💾 Guardar")
        borrar = c2.form_submit_button("🗑️ Eliminar", disabled=(id_sel is None))

    data = {"equipo_id": equipo_id, "nombre": nombre, "orden": int(orden),
            "descripcion": descripcion, "imagen_url": imagen_url}

    if guardar and nombre:
        actualizar("etapas", id_sel, data) if id_sel else crear("etapas", data)
        st.success("Etapa guardada.")
        st.rerun()

    if borrar and id_sel:
        eliminar("etapas", id_sel)
        st.warning("Etapa eliminada.")
        st.rerun()


def gestionar_componentes():
    st.markdown("#### Componentes")
    equipos = listar("equipos", orden="nombre")
    if not equipos:
        st.info("Primero crea un equipo.")
        return
    equipo_id = st.selectbox("Equipo", [e["id"] for e in equipos],
                              format_func=lambda eid: next(e["nombre"] for e in equipos if e["id"] == eid),
                              key="equipo_para_componentes")
    etapas = listar("etapas", filtros={"equipo_id": equipo_id}, orden="orden")
    if not etapas:
        st.info("Este equipo no tiene etapas todavía.")
        return
    etapa_id = st.selectbox("Etapa", [e["id"] for e in etapas],
                             format_func=lambda eid: next(e["nombre"] for e in etapas if e["id"] == eid),
                             key="etapa_para_componentes")

    componentes = listar("componentes", filtros={"etapa_id": etapa_id}, orden="nombre")
    if componentes:
        st.dataframe(pd.DataFrame(componentes)[["nombre", "tipo", "codigo"]],
                     use_container_width=True, hide_index=True)

    id_sel, actual = _selector_registro(componentes, "nombre", "sel_componente")

    tipos = ["Bomba", "Tuberia", "Separador", "Precalentador", "Valvula", "Motor", "Otro"]
    with st.form("form_componente"):
        nombre = st.text_input("Nombre*", value=actual.get("nombre", ""))
        tipo = st.selectbox("Tipo", tipos, index=tipos.index(actual["tipo"]) if actual.get("tipo") in tipos else 0)
        codigo = st.text_input("Código", value=actual.get("codigo", ""))
        descripcion = st.text_area("Descripción", value=actual.get("descripcion", ""))
        imagen_url = st.text_input("URL de imagen de despiece", value=actual.get("imagen_url", ""))
        c1, c2 = st.columns(2)
        guardar = c1.form_submit_button("💾 Guardar")
        borrar = c2.form_submit_button("🗑️ Eliminar", disabled=(id_sel is None))

    data = {"etapa_id": etapa_id, "nombre": nombre, "tipo": tipo, "codigo": codigo,
            "descripcion": descripcion, "imagen_url": imagen_url}

    if guardar and nombre:
        actualizar("componentes", id_sel, data) if id_sel else crear("componentes", data)
        st.success("Componente guardado.")
        st.rerun()

    if borrar and id_sel:
        eliminar("componentes", id_sel)
        st.warning("Componente eliminado.")
        st.rerun()


def gestionar_repuestos():
    st.markdown("#### Repuestos / Partes críticas")
    equipos = listar("equipos", orden="nombre")
    if not equipos:
        st.info("Primero crea un equipo.")
        return
    equipo_id = st.selectbox("Equipo", [e["id"] for e in equipos],
                              format_func=lambda eid: next(e["nombre"] for e in equipos if e["id"] == eid),
                              key="equipo_para_repuestos")
    etapas = listar("etapas", filtros={"equipo_id": equipo_id}, orden="orden")
    if not etapas:
        st.info("Este equipo no tiene etapas.")
        return
    etapa_id = st.selectbox("Etapa", [e["id"] for e in etapas],
                             format_func=lambda eid: next(e["nombre"] for e in etapas if e["id"] == eid),
                             key="etapa_para_repuestos")
    componentes = listar("componentes", filtros={"etapa_id": etapa_id}, orden="nombre")
    if not componentes:
        st.info("Esta etapa no tiene componentes.")
        return
    componente_id = st.selectbox("Componente", [c["id"] for c in componentes],
                                  format_func=lambda cid: next(c["nombre"] for c in componentes if c["id"] == cid),
                                  key="componente_para_repuestos")

    repuestos = listar("repuestos", filtros={"componente_id": componente_id}, orden="nombre")
    if repuestos:
        st.dataframe(pd.DataFrame(repuestos)[["nombre", "tipo", "stock_actual", "punto_reorden", "costo_unitario"]],
                     use_container_width=True, hide_index=True)

    id_sel, actual = _selector_registro(repuestos, "nombre", "sel_repuesto")

    tipos = ["Sello Mecanico", "Rodamiento", "Empaque", "Kit", "Otro"]
    with st.form("form_repuesto"):
        nombre = st.text_input("Nombre*", value=actual.get("nombre", ""))
        tipo = st.selectbox("Tipo", tipos, index=tipos.index(actual["tipo"]) if actual.get("tipo") in tipos else 0)
        codigo = st.text_input("Código / SKU", value=actual.get("codigo", ""))
        costo_unitario = st.number_input("Costo unitario (S/)", min_value=0.0,
                                          value=float(actual.get("costo_unitario", 0)), step=0.5)
        punto_reorden = st.number_input("Punto de reorden", min_value=0.0,
                                         value=float(actual.get("punto_reorden", 0)), step=1.0)
        stock_minimo = st.number_input("Stock mínimo", min_value=0.0,
                                        value=float(actual.get("stock_minimo", 0)), step=1.0)
        imagen_url = st.text_input("URL de imagen", value=actual.get("imagen_url", ""))
        stock_inicial = None
        if not id_sel:
            stock_inicial = st.number_input(
                "Stock inicial", min_value=0.0, value=0.0, step=1.0,
                help="Solo se usa al crear. Después, ajusta el stock desde la pestaña Kardex.")
        c1, c2 = st.columns(2)
        guardar = c1.form_submit_button("💾 Guardar")
        borrar = c2.form_submit_button("🗑️ Eliminar", disabled=(id_sel is None))

    data = {"componente_id": componente_id, "nombre": nombre, "tipo": tipo, "codigo": codigo,
            "costo_unitario": costo_unitario, "punto_reorden": punto_reorden, "stock_minimo": stock_minimo,
            "imagen_url": imagen_url}
    if not id_sel:
        data["stock_actual"] = stock_inicial

    if guardar and nombre:
        actualizar("repuestos", id_sel, data) if id_sel else crear("repuestos", data)
        st.success("Repuesto guardado.")
        st.rerun()

    if borrar and id_sel:
        eliminar("repuestos", id_sel)
        st.warning("Repuesto eliminado.")
        st.rerun()


def render():
    st.header("🏗️ Jerarquía del equipo")
    sub = st.tabs(["Equipos", "Etapas", "Componentes", "Repuestos"])
    with sub[0]:
        gestionar_equipos()
    with sub[1]:
        gestionar_etapas()
    with sub[2]:
        gestionar_componentes()
    with sub[3]:
        gestionar_repuestos()
