import os, json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODELO = os.getenv("GEMINI_MODEL")

SOLICITUD = (
    "El sistema de matricula se cayo otra vez, es la tercera semana "
    "seguida y nadie del area de sistemas responde los correos."
)

SISTEMA_A = """Eres un clasificador de incidencias universitarias.
Devuelve UNICAMENTE un objeto JSON con estas claves:
categoria (facturacion | soporte_tecnico | matricula | otro)
urgencia (entero del 1 al 5)
requiere_tecnico (true o false)
resumen (maximo 140 caracteres)
No agregues ningun texto antes ni despues."""

config_a = types.GenerateContentConfig(system_instruction=SISTEMA_A, temperature=0.0)
r = cliente.models.generate_content(model=MODELO, contents=SOLICITUD, config=config_a)

print("--- TEXTO CRUDO QUE DEVOLVIO EL MODELO (PARTE A) ---")
print(repr(r.text))

def limpiar_json(texto: str) -> str:
    t = (texto or "").strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else t
        t = t.rsplit("```", 1)[0]
    return t.strip()

try:
    datos = json.loads(limpiar_json(r.text))
    print("Categoria extraida de Parte A:", datos["categoria"])
except Exception as e:
    print("Error esperado al decodificar Parte A:", type(e).__name__)

ESQUEMA = {
    "type": "object",
    "properties": {
        "categoria": {
            "type": "string",
            "enum": ["facturacion", "soporte_tecnico", "matricula", "otro"],
        },
        "urgencia": {"type": "integer"},
        "requiere_tecnico": {"type": "boolean"},
        "resumen": {"type": "string"},
    },
    "required": ["categoria", "urgencia", "requiere_tecnico", "resumen"],
}

config_b = types.GenerateContentConfig(
    system_instruction=SISTEMA_A,
    temperature=0.0,
    response_mime_type="application/json",
    response_schema=ESQUEMA,
)
r2 = cliente.models.generate_content(model=MODELO, contents=SOLICITUD, config=config_b)

print("--- CON ESQUEMA FORZADO (PARTE B) ---")
print(r2.text)
datos2 = json.loads(r2.text)
print("categoria =", datos2["categoria"], "| urgencia =", datos2["urgencia"])
print("tipo de urgencia en Python:", type(datos2["urgencia"]))
