import json, pathlib
from google.genai import types

RUTA = pathlib.Path(__file__).resolve().parent.parent / "datos" / "tickets.json"

def consultar_ticket(codigo: str) -> dict:
    """Consulta el estado real de un ticket de soporte a partir de su codigo."""
    base = json.loads(RUTA.read_text(encoding="utf-8-sig"))
    return base.get(codigo.upper(), {"error": "No existe un ticket con ese codigo"})

def calcular_dias_habiles(dias_totales: int) -> dict:
    """Calcula cuantos de esos dias totales son dias habiles, asumiendo 5 de cada 7."""
    habiles = round(dias_totales * 5 / 7)
    return {"dias_totales": dias_totales, "dias_habiles_estimados": habiles}

DECLARACION_TICKET = types.FunctionDeclaration(
    name="consultar_ticket",
    description="Consulta el estado real, area, dias abierto y prioridad de un ticket de incidencia institucional a partir de su codigo, devolviendo los datos en formato JSON.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "codigo": types.Schema(
                type=types.Type.STRING,
                description="Codigo del ticket con formato TK-####, por ejemplo TK-1042",
            )
        },
        required=["codigo"],
    ),
)

DECLARACION_DIAS = types.FunctionDeclaration(
    name="calcular_dias_habiles",
    description="Calcula cuantos dias habiles (de lunes a viernes) equivalen a una cantidad de dias totales. Util para saber si un ticket lleva mucho tiempo abierto en dias laborables reales.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "dias_totales": types.Schema(
                type=types.Type.INTEGER,
                description="Cantidad de dias totales (calendario) a convertir en dias habiles",
            )
        },
        required=["dias_totales"],
    ),
)

HERRAMIENTAS = types.Tool(function_declarations=[DECLARACION_TICKET, DECLARACION_DIAS])
FUNCIONES = {
    "consultar_ticket": consultar_ticket,
    "calcular_dias_habiles": calcular_dias_habiles,
}
