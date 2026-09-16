import os, json, time, re
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import ValidationError

from nucleo.esquemas import Ticket
from nucleo.robustez import llamar_con_reintentos
from nucleo.costos import estimar_costo
from nucleo.trazas import registrar
from nucleo.herramientas import HERRAMIENTAS, FUNCIONES

load_dotenv()

cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODELO = os.getenv("GEMINI_MODEL")

PATRON_TICKET = re.compile(r"TK-\d{3,5}", re.IGNORECASE)

def clasificar(texto: str):
    config = types.GenerateContentConfig(
        system_instruction="Clasifica la incidencia universitaria recibida.",
        temperature=0.0,
        response_mime_type="application/json",
        response_schema=Ticket,
    )
    r, intentos = llamar_con_reintentos(
        lambda: cliente.models.generate_content(model=MODELO, contents=texto, config=config)
    )
    return Ticket.model_validate(json.loads(r.text)), r

def consultar_si_menciona_ticket(texto: str):
    """Si el texto menciona un codigo, usa la herramienta para traer el dato real."""
    encontrado = PATRON_TICKET.search(texto)
    if not encontrado:
        return None
    # TODO 1 completado: ejecuta la herramienta con el codigo encontrado
    return FUNCIONES["consultar_ticket"](encontrado.group(0).upper())

def procesar(texto: str) -> None:
    print("=" * 60)
    print("SOLICITUD:", texto[:70])
    inicio = time.perf_counter()
    try:
        ticket, r = clasificar(texto)
        ms = int((time.perf_counter() - inicio) * 1000)
        u = r.usage_metadata
        # TODO 2 completado: calcula el costo de esta llamada
        costo = estimar_costo(MODELO, u.prompt_token_count, u.candidates_token_count or 0)

        print(f"  categoria........: {ticket.categoria}")
        print(f"  urgencia.........: {ticket.urgencia}/5")
        print(f"  requiere tecnico : {ticket.requiere_tecnico}")
        print(f"  resumen..........: {ticket.resumen}")

        extra = consultar_si_menciona_ticket(texto)
        if extra:
            print(f"  dato real del sistema: {extra}")

        print(f"  tokens {u.prompt_token_count}+{u.candidates_token_count} | costo {costo:.6f} USD | {ms} ms")

        registrar(modelo=MODELO, operacion="clasificar",
                  tok_in=u.prompt_token_count,
                  tok_out=u.candidates_token_count or 0,
                  costo_usd=round(costo, 6), ok=True, ms=ms,
                  categoria=ticket.categoria, urgencia=ticket.urgencia)

    except ValidationError as e:
        print("  RESPUESTA INVALIDA -> marcada para revision humana")
        registrar(modelo=MODELO, operacion="clasificar", ok=False,
                  error="validacion", detalle=str(e.errors()[0]["msg"]))

    except Exception as e:
        print(f"  ERROR NO RECUPERABLE: {type(e).__name__}")
        registrar(modelo=MODELO, operacion="clasificar", ok=False,
                  error=type(e).__name__)

if __name__ == "__main__":
    with open("solicitudes.txt", encoding="utf-8-sig") as f:
        ENTRADAS = [linea.strip() for linea in f if linea.strip()]
    for texto in ENTRADAS:
        procesar(texto)
    print("=" * 60)
    print("Listo. Revise logs/trazas.jsonl")

