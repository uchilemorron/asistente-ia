import os, time
from dotenv import load_dotenv
from google import genai
from google.genai import types

from nucleo.herramientas import HERRAMIENTAS, FUNCIONES
from nucleo.robustez import llamar_con_reintentos

load_dotenv()

cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODELO = os.getenv("GEMINI_MODEL")

config = types.GenerateContentConfig(
    tools=[HERRAMIENTAS],
    temperature=0.0,
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)

def responder(pregunta: str) -> str:
    historial = [types.Content(role="user", parts=[types.Part.from_text(text=pregunta)])]

    for _ in range(5):  # tope de seguridad para no encadenar infinitamente
        r, _ = llamar_con_reintentos(
            lambda: cliente.models.generate_content(model=MODELO, contents=historial, config=config)
        )

        if not r.function_calls:
            return "(sin herramienta) " + (r.text or "").strip() if not historial[1:] else (r.text or "").strip()

        historial.append(r.candidates[0].content)
        partes_respuesta = []

        for llamada in r.function_calls:
            while isinstance(llamada, list):
                llamada = llamada[0]
            print(f"  -> el modelo pide: {llamada.name}({dict(llamada.args)})")
            funcion = FUNCIONES[llamada.name]
            resultado = funcion(**dict(llamada.args))
            print(f"  -> Python devuelve: {resultado}")
            partes_respuesta.append(types.Part.from_function_response(
                name=llamada.name, response={"resultado": resultado}
            ))

        historial.append(types.Content(role="user", parts=partes_respuesta))

    return "(no se pudo completar tras varios encadenamientos)"

for pregunta in [
    "Como va el ticket TK-1042?",
    "Y el TK-9999?",
    "Que es una API? Responde en una frase.",
    "El ticket TK-1042 lleva 3 dias abierto. Cuantos de esos son dias habiles, y como va el ticket?",
]:
    print("=" * 55)
    print("PREGUNTA:", pregunta)
    print("RESPUESTA:", responder(pregunta))
    time.sleep(15)
