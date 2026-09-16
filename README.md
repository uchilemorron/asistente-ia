# Asistente de solicitudes con IA generativa

Clasifica solicitudes de soporte usando un modelo de lenguaje por API, valida la salida contra un esquema, consulta datos reales mediante una herramienta invocable y registra tokens y costos de cada llamada.

## Requisitos
Python 3.10+ - pip install -r requirements.txt

## Configuracion
Copie .env.example a .env y complete su propia API key de Google Gemini.
La clave NO esta en este repositorio y nunca debe estarlo.

## Uso
python app.py

## Estructura
asistente-ia/
- app.py                  (Flujo integrado final, Etapa 9)
- e00_verificar.py        (Verificacion de credenciales y modelos)
- e01_conexion.py         (Primera conexion a la API)
- e02_parametros.py       (Parametros de generacion y mensaje de sistema)
- e03_estructurado.py     (Salida estructurada JSON)
- e04_validacion.py       (Validacion con Pydantic)
- e05_errores.py          (Reintentos y espera exponencial)
- e06_costos.py           (Metricas de costos y trazas)
- e07_streaming.py        (Comparacion con-sin streaming)
- e08_herramienta.py      (Function calling manual de 4 pasos)
- requirements.txt
- .env.example
- nucleo/
  - esquemas.py           (Contrato Pydantic Ticket)
  - robustez.py           (Reintentos con espera exponencial)
  - costos.py             (Calculo de costos por tokens)
  - trazas.py             (Registro de auditoria)
  - herramientas.py       (Herramientas consultar_ticket y calcular_dias_habiles)
  - simulado.py           (Cliente simulado, Anexo A, para contingencias de cuota)
- datos/
  - tickets.json          (Base de datos ficticia de tickets)
- precios.json            (Tarifario por modelo)
- solicitudes.txt         (Entradas externas para app.py, Reto Rapido Etapa 9)
- logs/
  - trazas.jsonl          (Registro de auditoria, no versionado, excluido por .gitignore)

## Costos observados
En pruebas realizadas durante el desarrollo (Etapa 6), cada llamada de clasificacion tuvo un costo estimado de entre 0.00008 y 0.00016 USD, dependiendo del tamaño de la solicitud y de la cantidad de tokens generados. Proyectando ese consumo a 20 000 llamadas, el costo estimado ronda entre 1.6 y 3.2 USD.

## Nota sobre la Etapa 8
Debido al agotamiento de la cuota gratuita diaria de la API en la cuenta principal, la Etapa 8 (function calling) se ejecuto utilizando una clave de API generada desde una cuenta de Google personal adicional, unicamente para efectos de continuidad academica, tal como contempla la guia de laboratorio. El codigo del asistente y la logica de la herramienta permanecen identicos; solo cambio la credencial de acceso usada durante la ejecucion.

## Reto Rapido Etapa 5
La espera exponencial es mejor que una espera fija porque incrementa el tiempo de descanso de forma progresiva, permitiendo que el servidor saturado se recupere en lugar de seguir bombardeandolo con solicitudes consecutivas inmediatas.

## Reto Rapido Etapa 7
El streaming conviene en la interfaz conversacional del asistente, donde el usuario espera ver la respuesta mientras se genera. No conviene en el proceso de clasificacion masiva de tickets (etapas 4 y 6), porque ahi nadie esta mirando la pantalla y lo unico que importa es el resultado final completo.
