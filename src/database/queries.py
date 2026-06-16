from typing import Optional
from src.database.connection import get_supabase


def buscar_recursos(query: str) -> list[dict]:
    supabase = get_supabase()
    result = (
        supabase.table("recursos")
        .select("*")
        .ilike("nombre", f"%{query}%")
        .execute()
    )
    return result.data


def consultar_inventario(categoria: Optional[str] = None) -> list[dict]:
    supabase = get_supabase()
    query = supabase.table("recursos").select("*")
    if categoria:
        query = query.eq("categoria", categoria)
    result = query.order("created_at", desc=True).execute()
    return result.data


def registrar_recurso(
    nombre: str,
    cantidad: int,
    descripcion: str = "",
    categoria: str = "",
    estado: str = "disponible",
    ubicacion: str = "",
    unidad: str = "unidad",
) -> list[dict]:
    supabase = get_supabase()
    data = {
        "nombre": nombre,
        "cantidad": cantidad,
        "descripcion": descripcion,
        "categoria": categoria,
        "estado": estado,
        "ubicacion": ubicacion,
        "unidad": unidad,
    }
    result = supabase.table("recursos").insert(data).execute()
    return result.data


def buscar_relacionados(categoria: str) -> list[dict]:
    supabase = get_supabase()
    result = (
        supabase.table("recursos")
        .select("*")
        .eq("categoria", categoria)
        .execute()
    )
    return result.data


def consultar_proyectos() -> list[dict]:
    supabase = get_supabase()
    result = (
        supabase.table("proyectos")
        .select("*")
        .order("fecha_inicio", desc=True)
        .execute()
    )
    return result.data


def guardar_conversacion(
    telegram_user_id: str,
    mensaje_usuario: str,
    respuesta_sistema: str,
    tipo_entrada: str = "texto",
    intencion_detectada: Optional[str] = None,
):
    supabase = get_supabase()
    data = {
        "telegram_user_id": telegram_user_id,
        "mensaje_usuario": mensaje_usuario,
        "respuesta_sistema": respuesta_sistema,
        "tipo_entrada": tipo_entrada,
    }
    if intencion_detectada:
        data["intencion_detectada"] = intencion_detectada
    supabase.table("conversaciones").insert(data).execute()


def obtener_conversaciones(telegram_user_id: str, limite: int = 10) -> list[dict]:
    supabase = get_supabase()
    result = (
        supabase.table("conversaciones")
        .select("*")
        .eq("telegram_user_id", telegram_user_id)
        .order("fecha", desc=True)
        .limit(limite)
        .execute()
    )
    return list(reversed(result.data))
