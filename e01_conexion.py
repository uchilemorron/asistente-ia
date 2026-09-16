import os
from dotenv import load_dotenv
from google import genai
 
load_dotenv()
if os.getenv("PROVEEDOR", "real") == "simulado":
    from nucleo.simulado import ClienteSimulado
    cliente = ClienteSimulado()
else:
    cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODELO = os.getenv("GEMINI_MODEL")
 
# Reto r?pido: pregunta personalizada con respuesta conocida
respuesta = cliente.models.generate_content(
    model=MODELO,
    contents="Responde en una sola frase: ?De qu? color es el cielo en un d?a despejado?",
)
 
print("=== RESPUESTA DEL MODELO (RETO ETAPA 1) ===")
print(respuesta.text)
