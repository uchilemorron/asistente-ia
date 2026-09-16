import time, random
from google.genai import errors
 
REINTENTABLES = {429, 500, 502, 503, 504}
 
def llamar_con_reintentos(funcion, intentos: int = 3, base: float = 1.0):
    """Ejecuta funcion(). Reintenta solo si el error lo amerita."""
    ultimo = None
    for i in range(intentos):
        try:
            return funcion(), i + 1
        except errors.APIError as e:
            ultimo = e
            codigo = getattr(e, "code", None)
            if codigo not in REINTENTABLES:
                raise
            espera = base ** i + random.uniform(0, 0.4)
            print(f"  aviso: error {codigo}. Reintento {i+1}/{intentos} en {espera:.1f}s")
            time.sleep(espera)
    raise ultimo
