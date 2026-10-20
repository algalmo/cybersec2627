"""Pruebas de conectividad contra la intranet, a través de la pasarela HTTPS.

Comprueba que:
  - la pasarela responde por HTTPS,
  - la API exige token (deniega sin él),
  - los códigos HTTP son los esperados,
y genera un pequeño informe en informe.json.
"""
import json
import requests

# Atacamos SIEMPRE a la pasarela (Nginx), nunca a la API directamente.
BASE = "https://localhost:8443"
TOKEN = {"X-Token": "secreto-de-laboratorio"}

# Certificado autofirmado de laboratorio: por eso verify=False (solo en pruebas).
requests.packages.urllib3.disable_warnings()

PRUEBAS = [
    ("Salud del servicio (sin token)",         lambda: requests.get(f"{BASE}/salud", verify=False),                 200),
    ("Listar empleados SIN token (denegado)",  lambda: requests.get(f"{BASE}/empleados", verify=False),             401),
    ("Listar empleados CON token",             lambda: requests.get(f"{BASE}/empleados", headers=TOKEN, verify=False), 200),
    ("Empleado existente CON token",           lambda: requests.get(f"{BASE}/empleados/1", headers=TOKEN, verify=False), 200),
    ("Empleado inexistente CON token (404)",   lambda: requests.get(f"{BASE}/empleados/99", headers=TOKEN, verify=False), 404),
]

def ejecutar() -> list[dict]:
    resultados = []
    for descripcion, llamada, esperado in PRUEBAS:
        try:
            codigo = llamada().status_code
        except requests.RequestException:
            codigo = None
        resultados.append({
            "prueba": descripcion,
            "esperado": esperado,
            "obtenido": codigo,
            "resultado": "OK" if codigo == esperado else "FALLO",
        })
    return resultados

if __name__ == "__main__":
    resultados = ejecutar()
    print(f"{'PRUEBA':42} {'ESPERA':7} {'OBTIENE':8} RESULTADO")
    print("-" * 70)
    for r in resultados:
        print(f"{r['prueba']:42} {r['esperado']:<7} {str(r['obtenido']):<8} {r['resultado']}")
    aciertos = sum(1 for r in resultados if r["resultado"] == "OK")
    print("-" * 70)
    print(f"Total: {aciertos}/{len(resultados)} pruebas correctas")
    with open("informe.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print("Informe guardado en informe.json")
