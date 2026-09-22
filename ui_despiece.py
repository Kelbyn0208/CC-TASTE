"""
ui_despiece.py - Vista interactiva del despiece de un componente:
muestra la imagen y, al pasar el cursor sobre cada punto, el nombre
y stock del repuesto ubicado ahí.
"""
import streamlit as st
import streamlit.components.v1 as components
from db import listar


def _construir_html_despiece(imagen_url: str, puntos: list[dict]) -> str:
    marcadores = ""
    for p in puntos:
        marcadores += f"""
        <div class="punto" style="left:{p['pos_x']}%; top:{p['pos_y']}%;">
            <div class="etiqueta">
                <strong>{p['nombre']}</strong><br>
                Stock: {p.get('stock_actual', 0)} · Código: {p.get('codigo') or '-'}
            </div>
        </div>
        """
    return f"""
    <style>
        .contenedor {{
            position: relative;
            width: 100%;
            height: 520px;
            background-image: url('{imagen_url}');
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            background-color: #10141c;
            border-radius: 10px;
            border: 1px solid #2a2f3a;
        }}
        .punto {{
            position: absolute;
            width: 16px;
            height: 16px;
            background: #F2A93B;
            border: 2px solid #ffffff;
            border-radius: 50%;
            transform: translate(-50%, -50%);
            cursor: pointer;
            box-shadow: 0 0 6px rgba(242,169,59,0.8);
        }}
        .etiqueta {{
            visibility: hidden;
            opacity: 0;
            transition: opacity 0.15s;
            position: absolute;
            bottom: 22px;
            left: 50%;
            transform: translateX(-50%);
            background: #1E293B;
            color: #E2E8F0;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 13px;
            white-space: nowrap;
            box-shadow: 0 2px 8px rgba(0,0,0,0.4);
            z-index: 10;
        }}
        .punto:hover .etiqueta {{
            visibility: visible;
            opacity: 1;
        }}
    </style>
    <div class="contenedor">
        {marcadores}
    </div>
    """


def render():
    st.header("🖼️ Despiece interactivo")

    equipos = listar("equipos")
    if not equipos:
        st.info("Primero crea el equipo en la pestaña Jerarquía.")
        return
    equipo_id = equipos[0]["id"]

    etapas = listar("etapas", filtros={"equipo_id": equipo_id}, orden="orden")
    if not etapas:
        st.info("Aún no hay etapas registradas.")
        return
    etapa_id = st.selectbox("Etapa", [e["id"] for e in etapas],
                             format_func=lambda eid: next(e["nombre"] for e in etapas if e["id"] == eid))

    area_id = st.selectbox("Área", ["Mecánica", "Eléctrica", "Neumática", "Electrónica"])

    componentes = listar("componentes", filtros={"etapa_id": etapa_id, "area": area_id}, orden="nombre")
    if not componentes:
        st.info("Esta etapa no tiene componentes en esa área.")
        return
    componente_id = st.selectbox("Componente", [c["id"] for c in componentes],
                                  format_func=lambda cid: next(c["nombre"] for c in componentes if c["id"] == cid))
    componente = next(c for c in componentes if c["id"] == componente_id)

    if not componente.get("imagen_url"):
        st.warning(
            "Este componente no tiene imagen de despiece. Agrégala desde "
            "Jerarquía → Componentes, campo 'URL de imagen de despiece' "
            "(sube la imagen a Supabase Storage y pega aquí su URL pública)."
        )
        return

    repuestos = listar("repuestos", filtros={"componente_id": componente_id})
    puntos = [r for r in repuestos if r.get("pos_x") is not None and r.get("pos_y") is not None]

    html = _construir_html_despiece(componente["imagen_url"], puntos)
    components.html(html, height=540, scrolling=False)

    if not puntos:
        st.info(
            "Esta imagen todavía no tiene puntos interactivos. Edita cada repuesto desde "
            "Jerarquía → Repuestos, activa 'Punto interactivo' y define su posición X/Y (%) "
            "sobre la imagen (por ejemplo, abre la imagen en Paint/Preview, ubica el pixel del "
            "repuesto y calcula % = pixel / tamaño_total_de_ese_eje × 100)."
        )
    else:
        st.caption("Pasa el cursor sobre los puntos amarillos para ver el repuesto y su stock actual.")
