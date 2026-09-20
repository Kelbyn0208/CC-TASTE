"""
ui_reportes.py - Historial exportable a Excel y KPI de frecuencia de falla.
"""
import io
import streamlit as st
import pandas as pd
from db import historial_intervenciones, frecuencia_falla


def _historial_df() -> pd.DataFrame:
    datos = historial_intervenciones()
    filas = []
    for row in datos:
        etapa_nombre = (row.get("etapas") or {}).get("nombre")
        componente_nombre = (row.get("componentes") or {}).get("nombre")
        detalles = row.get("intervencion_repuestos") or []
        if detalles:
            for d in detalles:
                repuesto_nombre = (d.get("repuestos") or {}).get("nombre")
                filas.append({"Fecha": row["fecha"], "Etapa": etapa_nombre, "Componente": componente_nombre,
                              "Repuesto": repuesto_nombre, "Cantidad": d.get("cantidad"),
                              "Tipo": row["tipo"], "Observaciones": row.get("descripcion")})
        else:
            filas.append({"Fecha": row["fecha"], "Etapa": etapa_nombre, "Componente": componente_nombre,
                          "Repuesto": None, "Cantidad": None, "Tipo": row["tipo"],
                          "Observaciones": row.get("descripcion")})
    return pd.DataFrame(filas)


def _a_excel(df: pd.DataFrame) -> bytes:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Historial")
    return buffer.getvalue()


def render():
    st.header("📊 Historial y Reportes")
    sub = st.tabs(["Historial", "Frecuencia de falla por repuesto"])

    with sub[0]:
        df = _historial_df()
        if df.empty:
            st.info("Aún no hay intervenciones registradas.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.download_button("⬇️ Descargar en Excel", data=_a_excel(df),
                                file_name="historial_mantenimiento_taste.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    with sub[1]:
        datos = frecuencia_falla()
        if not datos:
            st.info("Aún no hay suficientes datos para calcular frecuencia de falla.")
        else:
            df2 = pd.DataFrame(datos)
            st.dataframe(df2, use_container_width=True, hide_index=True)
            if "repuesto_nombre" in df2.columns and "veces_cambiado" in df2.columns:
                st.bar_chart(df2.set_index("repuesto_nombre")["veces_cambiado"])
