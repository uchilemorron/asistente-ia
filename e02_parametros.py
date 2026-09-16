import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
 
load_dotenv()

if os.getenv("PROVEEDOR", "real") == "simulado":
    from nucleo.simulado import ClienteSimulado
    cliente = ClienteSimulado()
else:
    cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODELO = os.getenv("GEMINI_MODEL")
SOLICITUD = "El sistema de matricula se cayo otra vez, es la tercera semana seguida y nadie responde los correos."

# TODO 1: Mensaje de sistema con la frase del reto r?pido incorporada
SISTEMA = "Eres un clasificador de incidencias de una universidad. Devuelve exactamente tres l?neas: categoria, urgencia del 1 al 5 y requiere_tecnico (si/no). RESPONDE SIEMPRE EN MAY?SCULAS."
 
def clasificar(temperatura, maximo_tokens):
    config = types.GenerateContentConfig(
        system_instruction=SISTEMA,
        # TODO 2: Conexi?n de los par?metros
        temperature=temperatura,
        max_output_tokens=maximo_tokens,
    )
    return cliente.models.generate_content(model=MODELO, contents=SOLICITUD, config=config)
 
for etiqueta, temp, tope in [
    ("A  temp=0.0", 0.0, 200),
    ("B  temp=1.6", 1.6, 200),
    ("C  tope=15 ", 0.0, 15),
]:
    print("=" * 60)
    for intento in range(1, 4):
        r = clasificar(temp, tope)
        texto = (r.text or "(vac?o)").strip().replace("\n", " ")
        print(f"{etiqueta} | intento {intento} | {texto[:90]}")
        print(f"           finish_reason = {r.candidates[0].finish_reason}")
