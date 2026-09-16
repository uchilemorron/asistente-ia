import os, time
from dotenv import load_dotenv
from google import genai

load_dotenv()

cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODELO = os.getenv("GEMINI_MODEL")

PETICION = "Explica en unas 200 palabras por que conviene validar la salida de un modelo."

print("--- SIN STREAMING ---")
t0 = time.perf_counter()
r = cliente.models.generate_content(model=MODELO, contents=PETICION)
print(r.text)
print(f"Primer caracter visible a los {time.perf_counter() - t0:.2f} s")

print("\n--- CON STREAMING ---")
t0 = time.perf_counter()
primero = None
partes = []

for fragmento in cliente.models.generate_content_stream(model=MODELO, contents=PETICION):
    if fragmento.text:
        if primero is None:
            primero = time.perf_counter() - t0
        print(fragmento.text, end="", flush=True)
        partes.append(fragmento.text)

completo = "".join(partes)
print(f"\n\nPrimer caracter a los {primero:.2f} s | total {time.perf_counter() - t0:.2f} s")
print(f"Caracteres recibidos: {len(completo)}")
