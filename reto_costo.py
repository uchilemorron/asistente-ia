import json, pathlib
RUTA = pathlib.Path("logs/trazas.jsonl")
total = 0.0
with RUTA.open(encoding="utf-8") as f:
    for linea in f:
        total += json.loads(linea)["costo_usd"]
print(f"Costo total acumulado: {total:.6f} USD")
