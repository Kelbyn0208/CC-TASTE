"""
db.py - Capa de acceso a datos (Supabase) para el sistema TASTE.
Contiene funciones CRUD genéricas reutilizables por todas las pestañas
y algunas consultas específicas (historial, vistas, kardex).
"""

import streamlit as st
from supabase import create_client, Client


@st.cache_resource
def get_client() -> Client:
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])


sb = get_client()


# ============================ CRUD GENÉRICO ============================

def listar(tabla: str, filtros: dict | None = None, orden: str | None = None, columnas: str = "*") -> list[dict]:
    q = sb.table(tabla).select(columnas)
    if filtros:
        for col, val in filtros.items():
            q = q.eq(col, val)
    if orden:
        q = q.order(orden)
    return q.execute().data


def crear(tabla: str, data: dict) -> list[dict]:
    return sb.table(tabla).insert(data).execute().data


def actualizar(tabla: str, id_: str, data: dict) -> list[dict]:
    return sb.table(tabla).update(data).eq("id", id_).execute().data


def eliminar(tabla: str, id_: str) -> None:
    sb.table(tabla).delete().eq("id", id_).execute()


# ============================ CONSULTAS ESPECÍFICAS ============================

def historial_intervenciones() -> list[dict]:
    return (
        sb.table("intervenciones")
        .select(
            "id, fecha, tipo, descripcion, "
            "etapas(nombre), componentes(nombre), "
            "intervencion_repuestos(id, cantidad, repuestos(nombre))"
        )
        .order("fecha", desc=True)
        .execute()
        .data
    )


def frecuencia_falla() -> list[dict]:
    return sb.table("vw_frecuencia_falla_repuesto").select("*").execute().data


def repuestos_para_reponer() -> list[dict]:
    return sb.table("vw_repuestos_para_reponer").select("*").execute().data


def movimientos_kardex(repuesto_id: str | None = None) -> list[dict]:
    q = sb.table("kardex_movimientos").select("*, repuestos(nombre)").order("fecha", desc=True)
    if repuesto_id:
        q = q.eq("repuesto_id", repuesto_id)
    return q.execute().data
