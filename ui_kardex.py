"""
ui_kardex.py - Registro de entradas/salidas, alertas de stock e historial editable.
"""
import streamlit as st
import pandas as pd
from datetime import date
from db import listar, crear, actualizar, eliminar, movimientos_kardex, repuestos_para_reponer


def _lista_repuestos_con_etiqueta():
    """Repuestos con etiqueta 'Etapa > Componente > Repuesto' para el selector."""
    etapas = listar("etapas")
    componentes = listar("componentes")
    repuestos = listar("repuestos", filtros={"activo": True})

    etapa_por_id = {e["id"]: e for e in etapas}
    componente_por_id = {c["id"]: c for c in componentes}

    opciones = []
    for r in repuestos:
        c = componente_por_id.get(r["componente_id"], {})
        e = etapa_por_id.get(c.get("etapa_id"), {})
        etiqueta = f"{e.get('nombre', '?')} > {c.get('area', '?')} > {c.get('nombre', '?')} > {r['nombre']}"
        opciones.append((etiqueta, r))
    opciones.sort(key=lambda x: x[0])
    return opciones


def registrar_movimiento():
    st.markdown("#### Registrar entrada / salida")
    opciones = _lista_repuestos_con_etiqueta()
    if not opciones:
        st.info("Aún no hay repuestos registrados en la pestaña Jerarquía.")
        return

    etiquetas = [o[0] for o in opciones]
    idx = st.selectbox("Repuesto", range(len(etiquetas)), format_func=lambda i: etiquetas[i])
    repuesto = opciones[idx][1]

    st.caption(f"Stock actual: **{repuesto['stock_actual']}** · Punto de reorden: {repuesto['punto_reorden']}")

    with st.form("form_movimiento", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            tipo_movimiento = st.selectbox("Tipo de movimiento", ["ENTRADA", "SALIDA"])
            cantidad = st.number_input("Cantidad", min_value=0.01, value=1.0, step=1.0)
            fecha = st.date_input("Fecha", value=date.today())
        with col2:
            costo_unitario = st.number_input("Costo unitario (S/)", min_value=0.0,
                                              value=float(repuesto.get("costo_unitario", 0)), step=0.5)
            motivo = st.text_input("Motivo", placeholder="Compra, ajuste de inventario, etc.")
            documento_referencia = st.text_input("Documento de referencia (OC, OT, etc.)")
        usuario = st.text_input("Registrado por")
        enviado = st.form_submit_button("💾 Registrar movimiento")

    if enviado:
        crear("kardex_movimientos", {
            "repuesto_id": repuesto["id"], "tipo_movimiento": tipo_movimiento, "cantidad": cantidad,
            "costo_unitario": costo_unitario, "fecha": fecha.isoformat(), "motivo": motivo,
            "documento_referencia": documento_referencia, "usuario": usuario,
        })
        st.success("Movimiento registrado. El stock se actualizó automáticamente.")
        st.rerun()


def alertas_reorden():
    st.markdown("#### ⚠️ Repuestos por reponer")
    datos = repuestos_para_reponer()
    if not datos:
        st.success("Todos los repuestos están por encima de su punto de reorden.")
    else:
        st.dataframe(pd.DataFrame(datos), use_container_width=True, hide_index=True)


def historial_movimientos():
    st.markdown("#### Historial de movimientos")
    datos = movimientos_kardex()
    if not datos:
        st.info("Sin movimientos registrados todavía.")
        return

    for d in datos:
        d["repuesto_nombre"] = (d.get("repuestos") or {}).get("nombre")
    df = pd.DataFrame(datos)[["fecha", "repuesto_nombre", "tipo_movimiento", "cantidad",
                               "costo_unitario", "motivo", "documento_referencia", "usuario"]]
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("##### Corregir o eliminar un movimiento")
    etiquetas = {f"{d['fecha']} · {d.get('repuesto_nombre')} · {d['tipo_movimiento']} · {d['cantidad']}": d["id"]
                 for d in datos}
    sel = st.selectbox("Selecciona un movimiento", list(etiquetas.keys()))
    mov_id = etiquetas[sel]
    mov = next(d for d in datos if d["id"] == mov_id)

    with st.form("form_editar_mov"):
        cantidad = st.number_input("Cantidad", min_value=0.01, value=float(mov["cantidad"]))
        tipo_movimiento = st.selectbox("Tipo", ["ENTRADA", "SALIDA"],
                                        index=0 if mov["tipo_movimiento"] == "ENTRADA" else 1)
        motivo = st.text_input("Motivo", value=mov.get("motivo") or "")
        c1, c2 = st.columns(2)
        guardar = c1.form_submit_button("💾 Guardar cambios")
        borrar = c2.form_submit_button("🗑️ Eliminar movimiento")

    if guardar:
        actualizar("kardex_movimientos", mov_id, {
            "cantidad": cantidad, "tipo_movimiento": tipo_movimiento, "motivo": motivo,
        })
        st.success("Movimiento actualizado; el stock se recalculó automáticamente.")
        st.rerun()

    if borrar:
        eliminar("kardex_movimientos", mov_id)
        st.warning("Movimiento eliminado; el stock se revirtió automáticamente.")
        st.rerun()


def render():
    st.header("📦 Kardex de Repuestos")
    sub = st.tabs(["Registrar movimiento", "Alertas de reorden", "Historial"])
    with sub[0]:
        registrar_movimiento()
    with sub[1]:
        alertas_reorden()
    with sub[2]:
        historial_movimientos()
