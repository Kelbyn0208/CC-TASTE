"""
ui_reportes.py - Historial exportable a Excel y KPI de frecuencia de falla.
"""
import io
import streamlit as st
import pandas as pd
from fpdf import FPDF
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


def _a_pdf(df: pd.DataFrame, titulo: str) -> bytes:
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, titulo, ln=True)
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(0, 6, f"Generado: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.ln(2)

    columnas = list(df.columns)
    ancho_col = (pdf.w - 2 * pdf.l_margin) / len(columnas)

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(30, 41, 59)
    pdf.set_text_color(255, 255, 255)
    for col in columnas:
        pdf.cell(ancho_col, 7, str(col), border=1, fill=True)
    pdf.ln()

    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(0, 0, 0)
    for _, fila in df.iterrows():
        for col in columnas:
            valor = "" if pd.isna(fila[col]) else str(fila[col])
            pdf.cell(ancho_col, 6, valor[:45], border=1)
        pdf.ln()

    return bytes(pdf.output())


def render():
    st.header("Historial y Reportes")
    sub = st.tabs(["Historial", "Frecuencia de falla por repuesto"])

    with sub[0]:
        df = _historial_df()
        if df.empty:
            st.info("Aún no hay intervenciones registradas.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
            c1, c2 = st.columns(2)
            c1.download_button("Descargar en Excel", data=_a_excel(df),
                                file_name="historial_mantenimiento_taste.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            c2.download_button("Descargar en PDF",
                                data=_a_pdf(df, "Historial de Mantenimiento - Evaporador TASTE"),
                                file_name="historial_mantenimiento_taste.pdf", mime="application/pdf")

    with sub[1]:
        datos = frecuencia_falla()
        if not datos:
            st.info("Aún no hay suficientes datos para calcular frecuencia de falla.")
        else:
            df2 = pd.DataFrame(datos)
            st.dataframe(df2, use_container_width=True, hide_index=True)
            if "repuesto_nombre" in df2.columns and "veces_cambiado" in df2.columns:
                st.bar_chart(df2.set_index("repuesto_nombre")["veces_cambiado"])
