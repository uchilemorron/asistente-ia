import os
from dotenv import load_dotenv
from google import genai
from google.genai import errors
from nucleo.robustez import llamar_con_reintentos
 
load_dotenv()
cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODELO = os.getenv("GEMINI_MODEL")
 
def prueba(titulo, modelo, clave=None):
    print("=" * 55)
    print(titulo)
    c = genai.Client(api_key=clave) if clave else cliente
    try:
        r, intentos = llamar_con_reintentos(
            lambda: c.models.generate_content(model=modelo, contents="Di OK")
        )
        print(f"  OK en {intentos} intento(s): {r.text.strip()[:40]}")
    except errors.APIError as e:
        print(f"  FALL? con c?digo {getattr(e, 'code', '?')}: {str(e.message)[:90]}")
 
# Prueba 1: Llamada normal de control
prueba("1. Llamada normal", MODELO)

# Prueba 2: Forzar error 400 por modelo inexistente
prueba("2. Modelo inexistente (400, no se reintenta)", "gemini-flesh-99")

# TODO 2 completado: Prueba 3 inyectando una credencial falsa
prueba("3. Clave invalida (403/400, no se reintenta)", MODELO, clave="AIzaClaveFalsa123")
