import re
from collections import Counter
from pathlib import Path

PATRON_FALLO = re.compile(
    r"Failed password for (?P<usuario>\S+) from (?P<ip>\d+\.\d+\.\d+\.\d+)")

def analizar_log(ruta: Path, umbral: int = 3) -> None:
    texto = ruta.read_text(encoding="utf-8")

    fallos_por_ip: Counter[str] = Counter()
    usuarios_por_ip: dict[str, set[str]] = {}

    for linea in texto.splitlines():
        m = PATRON_FALLO.search(linea)
        if m:
            ip = m.group("ip")
            fallos_por_ip[ip] += 1
            usuarios_por_ip.setdefault(ip, set()).add(m.group("usuario"))

    print("=== Fallos de autenticación por IP ===")
    for ip, n in fallos_por_ip.most_common():
        usuarios = ", ".join(sorted(usuarios_por_ip[ip]))
        print(f"  {ip:16} {n} fallos  (usuarios: {usuarios})")

    print(f"\n=== IPs que superan el umbral ({umbral}) ===")
    hay_alertas = False
    for ip, n in fallos_por_ip.items():
        if n >= umbral:
            hay_alertas = True
            print(f"  [REVISAR] {ip}: {n} fallos con "
                  f"{len(usuarios_por_ip[ip])} usuario(s) distinto(s)")
    if not hay_alertas:
        print("  (ninguna)")

    print("\nNota: un umbral superado es un PATRÓN sospechoso que hay que verificar,")
    print("no una prueba de ataque por sí solo.")

if __name__ == "__main__":
    analizar_log(Path("auth.log"), umbral=3)
