import os
from dotenv import load_dotenv
from google import genai
 
load_dotenv()
clave = os.getenv("GEMINI_API_KEY")
modelo = os.getenv("GEMINI_MODEL")
 
print("Clave cargada:", "SI" if clave else "NO")
print("Longitud de la clave:", len(clave) if clave else 0)
print("Modelo configurado:", modelo)
print("-" * 50)
 
cliente = genai.Client(api_key=clave)
 
encontrados = []
for m in cliente.models.list():
    acciones = getattr(m, "supported_actions", None) or []
    if "generateContent" in acciones:
        encontrados.append(m.name)
 
print("Modelos disponibles para generar contenido:")
for nombre in encontrados[:15]:
    print("  -", nombre)
print("Total:", len(encontrados))
