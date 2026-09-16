import json, pathlib, datetime

CARPETA = pathlib.Path(__file__).resolve().parent.parent / "logs"
CARPETA.mkdir(exist_ok=True)
ARCHIVO = CARPETA / "trazas.jsonl"

def registrar(**campos):
    """Agrega una linea JSON al archivo de trazas."""
    campos["ts"] = datetime.datetime.now().isoformat(timespec="seconds")
    with ARCHIVO.open("a", encoding="utf-8") as f:
        f.write(json.dumps(campos, ensure_ascii=False) + "\n")
