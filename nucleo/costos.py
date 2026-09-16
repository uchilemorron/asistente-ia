import json, pathlib

RUTA = pathlib.Path(__file__).resolve().parent.parent / "precios.json"
PRECIOS = json.loads(RUTA.read_text(encoding="utf-8-sig"))

def estimar_costo(modelo: str, tok_entrada: int, tok_salida: int) -> float:
    clave = modelo.replace("models/", "")
    p = PRECIOS.get(clave, PRECIOS["_por_defecto"])
    return (tok_entrada / 1_000_000) * p["entrada"] + \
           (tok_salida / 1_000_000) * p["salida"]
