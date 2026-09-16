import os, time
from dotenv import load_dotenv
from google import genai

from nucleo.costos import estimar_costo
from nucleo.trazas import registrar

load_dotenv()

cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODELO = os.getenv("GEMINI_MODEL")

TEXTO = "Resume en dos frases que es el consumo de un modelo por API."

previo = cliente.models.count_tokens(model=MODELO, contents=TEXTO)
print("Tokens que voy a enviar:", previo.total_tokens)

inicio = time.perf_counter()
r = cliente.models.generate_content(model=MODELO, contents=TEXTO)
ms = int((time.perf_counter() - inicio) * 1000)

u = r.usage_metadata
tok_in = u.prompt_token_count
tok_out = u.candidates_token_count or 0

costo = estimar_costo(MODELO, tok_in, tok_out)

print(f"entrada={tok_in} salida={tok_out} total={u.total_token_count}")
print(f"costo estimado = {costo:.6f} USD | latencia = {ms} ms")
print(f"proyeccion a 20 000 llamadas = {costo * 20_000:.2f} USD")

registrar(modelo=MODELO, operacion="resumen", tok_in=tok_in, tok_out=tok_out,
          costo_usd=round(costo, 6), ok=True, intentos=1, ms=ms)

print("Traza escrita en logs/trazas.jsonl")
