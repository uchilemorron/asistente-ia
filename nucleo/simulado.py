import json, random, types as pytypes
 
RESPUESTAS = {
    "cielo": "El cielo en un dia despejado es de color azul debido a la dispersion de la luz solar por la atmosfera.",
    "incidencia": "CATEGORIA: MATRICULA\nURGENCIA: 4\nREQUIERE_TECNICO: SI"
}
 
class RespuestaSimulada:
    def __init__(self, texto, reason="STOP"):
        self.text = texto
        self.candidates = [pytypes.SimpleNamespace(finish_reason=reason)]
 
class ModelosSimulados:
    def generate_content(self, model=None, contents=None, config=None):
        tope = getattr(config, "max_output_tokens", 200)
        solicitud_texto = str(contents).lower()
        
        # Si la consulta contiene "cielo", responde de forma exacta sobre el cielo
        if "cielo" in solicitud_texto:
            return RespuestaSimulada(RESPUESTAS["cielo"])
            
        # Comportamiento para la Etapa 2
        if tope == 15:
            return RespuestaSimulada("CATEGORIA: MATR", "MAX_TOKENS")
            
        return RespuestaSimulada(RESPUESTAS["incidencia"])
 
class ClienteSimulado:
    def __init__(self, **kwargs):
        self.models = ModelosSimulados()
