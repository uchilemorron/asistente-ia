import os, json, time
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
from pydantic import ValidationError

from nucleo.esquemas import Ticket

load_dotenv()

cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODELO = os.getenv("GEMINI_MODEL")

ESQUEMA_GENERACION = {
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

def clasificar(texto: str, correccion: str = "") -> Ticket:
    config = types.GenerateContentConfig(
        system_instruction="Clasifica la incidencia universitaria recibida." + correccion,
        temperature=0.0,
        response_mime_type="application/json",
        response_schema=ESQUEMA_GENERACION,
    )
    r = cliente.models.generate_content(model=MODELO, contents=texto, config=config)
    bruto = json.loads(r.text)
    return Ticket.model_validate(bruto)

def clasificar_con_reintento(texto: str) -> Ticket | None:
    try:
        return clasificar(texto)
    except ValidationError as e:
        print("Primera validacion fallida. Reintentando con la correccion...")
        aviso = f"\nLa respuesta anterior fue invalida por: {e.errors()[0]['msg']}. Corrigelo."
        try:
            return clasificar(texto, aviso)
        except ValidationError:
            print("Fallo tambien el reintento: caso marcado para revision humana.")
            return None
    except errors.APIError as e:
        print(f"Fallo de la API (codigo {getattr(e, 'code', '?')}), no de validacion. Se omite este caso.")
        return None

CASOS = [
    "El sistema de matricula se cayo otra vez, tercera semana seguida.",
    "Buenos dias, queria consultar el horario de la biblioteca.",
    "Me cobraron dos veces la cuota de junio y nadie me responde.",
]

for texto in CASOS:
    t = clasificar_con_reintento(texto)
    if t:
        print(f"[{t.categoria:16}] urgencia={t.urgencia} tecnico={t.requiere_tecnico} :: {t.resumen}")
    else:
        print("[SIN CLASIFICAR] requiere revision humana")
    time.sleep(4)  # pausa defensiva para no chocar con el limite de cuota
