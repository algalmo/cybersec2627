import json
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger("defensa")

# Evidencias que han recogido los laboratorios anteriores, ya resumidas.
# Cada una indica: de qué fuente viene, a qué IP señala y qué se observó.
evidencias = [
    {"fuente": "logs",     "ip": "203.0.113.9", "hecho": "5 fallos de login"},
    {"fuente": "red",      "ip": "203.0.113.9", "hecho": "escaneo de 4 puertos"},
    {"fuente": "archivos", "ip": "203.0.113.9", "hecho": "modificó /etc/passwd"},
    {"fuente": "red",      "ip": "10.0.0.5",    "hecho": "1 conexión al puerto 80"},
]

# Agrupamos las evidencias por IP.
senales_por_ip: dict[str, list[dict]] = {}
for e in evidencias:
    senales_por_ip.setdefault(e["ip"], []).append(e)

# Regla de correlación: cuantas más fuentes distintas señalan a una IP, más grave.
def gravedad(n_evidencias: int) -> str:
    if n_evidencias >= 3:
        return "CRITICA"
    if n_evidencias == 2:
        return "ALTA"
    return "BAJA"

alertas = []
for ip, lista in senales_por_ip.items():
    nivel = gravedad(len(lista))
    alerta = {"ip": ip, "gravedad": nivel, "evidencias": [e["hecho"] for e in lista]}
    alertas.append(alerta)
    if nivel in ("ALTA", "CRITICA"):
        log.warning("%s en %s -> %s", nivel, ip, ", ".join(alerta["evidencias"]))

# Guardamos el informe en JSON para que otra herramienta pueda procesarlo.
with open("informe.json", "w", encoding="utf-8") as f:
    json.dump(alertas, f, indent=2, ensure_ascii=False)

print(f"\n{len(alertas)} IPs analizadas. Informe guardado en informe.json")
