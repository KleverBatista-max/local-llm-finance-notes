# local-llm-finance-notes

**ES:** Notas y un script pequeño de mi intento (abril 2026) de clasificar movimientos bancarios con un modelo que corre en mi propia PC, sin mandar nada a la nube.
**EN:** Notes and a small script from my April 2026 attempt to classify bank transactions with a model running on my own PC, nothing sent to the cloud.

## Qué monté / What I set up

- **Ollama** con `qwen2.5:7b-instruct` en una PC de escritorio con GPU modesta (poca VRAM, contexto de 8k). Mi [`Modelfile`](Modelfile) está en el repo.
- **OpenClaw** (agente) corriendo dentro de un **sandbox en Docker**, con un canal de WhatsApp restringido a mi número.
- Una capa propia en Python/Bash: lectura de los correos del banco por IMAP cada minuto, parser de plantillas, transacciones en JSONL y una bitácora de cada cambio.

## Qué salió mal / What went wrong

Lo cuento porque es lo que más me enseñó:

1. **El modelo de 7B se inventaba cosas** (comercios, categorías). Bajar la temperatura ayudó poco.
2. **Permisos del socket de Docker** y un sandbox sin `python3`: el agente no podía escribir los archivos.
3. **Sin git**: un archivo de 490 líneas se sobrescribió con un stub y el PC se dañó sin respaldo.
4. Nunca llegó a ser estable. Lo reemplacé por un sistema con parsers probados (Cuadra, [repo](https://github.com/KleverBatista-max/cuadra)).

## Lo que aprendí (y lo que hace `clasificar.py`)

El modelo **solo propone** una categoría de una **lista cerrada**; si responde algo fuera de la lista o JSON roto, el movimiento queda como `desconocido` para que lo revise una persona. El modelo nunca escribe datos por su cuenta.

```bash
ollama create finanzas -f Modelfile
python3 clasificar.py examples/movimientos.json --modelo finanzas
python3 -m unittest            # pruebas de la validación
```

Solo usa la biblioteca estándar de Python. Los datos de `examples/` son inventados.

> Honestidad: las pruebas cubren la validación y probé el flujo completo contra un servidor falso que imita la API de Ollama. No incluyo resultados de precisión del modelo real porque no hice una medición formal.

MIT
