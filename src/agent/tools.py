from langchain.tools import Tool, StructuredTool
from src.database import queries as db


def buscar_recurso(query: str) -> str:
    resultados = db.buscar_recursos(query)
    if not resultados:
        return f"No se encontraron recursos que coincidan con '{query}'."
    lines = ["**Recursos encontrados:**"]
    for r in resultados:
        unidad = r.get("unidad") or "unidad"
        line = f"- {r['nombre']}: {r['cantidad']} {unidad} ({r['estado']})"
        if r.get("categoria"):
            line += f" [{r['categoria']}]"
        if r.get("ubicacion"):
            line += f" - Ubicación: {r['ubicacion']}"
        lines.append(line)
    return "\n".join(lines)


def consultar_inventario(categoria: str = "") -> str:
    cat = categoria.strip() or None
    resultados = db.consultar_inventario(categoria=cat)
    if not resultados:
        if cat:
            return f"No hay recursos registrados en la categoría '{cat}'."
        return "No hay recursos registrados en el inventario."
    lines = ["**Inventario completo:**"]
    for r in resultados:
        unidad = r.get("unidad") or "unidad"
        line = f"- {r['nombre']}: {r['cantidad']} {unidad} | {r['estado']}"
        if r.get("categoria"):
            line += f" | Cat: {r['categoria']}"
        if r.get("ubicacion"):
            line += f" | Ub: {r['ubicacion']}"
        lines.append(line)
    return "\n".join(lines)


def registrar_recurso(
    nombre: str,
    cantidad: int,
    descripcion: str = "",
    categoria: str = "",
    estado: str = "disponible",
    ubicacion: str = "",
    unidad: str = "unidad",
) -> str:
    if not nombre or cantidad <= 0:
        return "Error: debe proporcionar un nombre válido y una cantidad mayor a cero."
    db.registrar_recurso(nombre, cantidad, descripcion, categoria, estado, ubicacion, unidad)
    return f"**Recurso registrado correctamente:**\n- {nombre}: {cantidad} {unidad}\n- Estado: {estado}\n- Categoría: {categoria or 'Sin categoría'}"


def buscar_relacionados(categoria: str) -> str:
    resultados = db.buscar_relacionados(categoria)
    if not resultados:
        return f"No se encontraron recursos en la categoría '{categoria}'."
    lines = [f"**Recursos en categoría '{categoria}':**"]
    for r in resultados:
        unidad = r.get("unidad") or "unidad"
        lines.append(f"- {r['nombre']}: {r['cantidad']} {unidad} ({r['estado']})")
    return "\n".join(lines)


def consultar_proyectos(query: str = "") -> str:
    resultados = db.consultar_proyectos()
    if not resultados:
        return "No hay proyectos registrados."
    lines = ["**Proyectos anteriores:**"]
    for p in resultados:
        desc = p.get("descripcion") or "Sin descripción"
        est = p.get("estado") or ""
        lines.append(f"- **{p['nombre']}**: {desc}")
        if p.get("responsable"):
            lines.append(f"  Responsable: {p['responsable']}")
        if est:
            lines.append(f"  Estado: {est}")
        if p.get("fecha_inicio"):
            lines.append(f"  Inicio: {p['fecha_inicio']}")
    return "\n".join(lines)


buscar_tool = Tool(
    name="Buscar Recurso",
    func=buscar_recurso,
    description=(
        "Busca un recurso específico en el inventario por su nombre. "
        "Útil cuando el usuario pregunta por un recurso concreto. "
        "Input: el nombre del recurso a buscar."
    ),
)

inventario_tool = Tool(
    name="Consultar Inventario",
    func=consultar_inventario,
    description=(
        "Obtiene una lista de todos los recursos disponibles en el inventario. "
        "Acepta una categoría opcional para filtrar. "
        "Input: nombre de categoría (opcional, vacío para todo el inventario)."
    ),
)

registrar_tool = StructuredTool.from_function(
    func=registrar_recurso,
    name="Registrar Recurso",
    description=(
        "Registra un nuevo recurso en el inventario. "
        "Parámetros: nombre (obligatorio), cantidad (obligatorio, >0), "
        "descripcion (opcional), categoria (opcional, infiere del nombre), "
        "estado (opcional, por defecto 'disponible'), ubicacion (opcional), "
        "unidad (opcional, por defecto 'unidad')."
    ),
)

relacionados_tool = Tool(
    name="Buscar Recursos Relacionados",
    func=buscar_relacionados,
    description=(
        "Busca recursos que pertenecen a una misma categoría. "
        "Útil para encontrar recursos similares. "
        "Input: nombre de la categoría."
    ),
)

proyectos_tool = Tool(
    name="Consultar Proyectos Anteriores",
    func=consultar_proyectos,
    description=(
        "Muestra la lista de proyectos anteriores registrados en el sistema. "
        "Input: cualquier texto (se ignora, siempre devuelve todos los proyectos)."
    ),
)

tools = [
    buscar_tool,
    inventario_tool,
    registrar_tool,
    relacionados_tool,
    proyectos_tool,
]
