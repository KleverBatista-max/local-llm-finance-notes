#!/usr/bin/env python3
"""Clasifica movimientos bancarios con un LLM local (Ollama). Solo biblioteca estandar.

Uso:  python3 clasificar.py examples/movimientos.json [--modelo qwen2.5:7b-instruct]

Regla de diseno (la leccion del intento anterior): el modelo SOLO propone una categoria
de una lista cerrada. Si responde algo fuera de la lista o JSON roto, el movimiento queda
como "desconocido" y lo revisa una persona. El modelo nunca escribe datos por su cuenta.
"""
import argparse, json, sys, urllib.request

CATEGORIAS = ["supermercado", "transporte", "restaurante", "servicios",
              "transferencia_interna", "salud", "otros", "desconocido"]
URL = "http://localhost:11434/api/chat"


def preguntar(mov, modelo, url=URL):
    prompt = (f"Categorias permitidas: {', '.join(CATEGORIAS)}.\n"
              f"Movimiento: {json.dumps(mov, ensure_ascii=False)}\n"
              'Responde {"categoria": "<una de la lista>"}')
    cuerpo = json.dumps({"model": modelo, "stream": False, "format": "json",
                         "options": {"temperature": 0.1},
                         "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(url, cuerpo, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)["message"]["content"]


def validar(texto):
    try:
        cat = json.loads(texto).get("categoria")
    except (ValueError, AttributeError):
        return "desconocido"
    return cat if cat in CATEGORIAS else "desconocido"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("archivo")
    ap.add_argument("--modelo", default="qwen2.5:7b-instruct")
    ap.add_argument("--url", default=URL)
    a = ap.parse_args()
    for mov in json.load(open(a.archivo, encoding="utf-8")):
        try:
            cat = validar(preguntar(mov, a.modelo, a.url))
        except OSError as e:
            sys.exit(f"No pude hablar con Ollama en {a.url}: {e}")
        print(f"{cat:22} {mov['comercio']}  {mov['monto']:.2f}")


if __name__ == "__main__":
    main()
