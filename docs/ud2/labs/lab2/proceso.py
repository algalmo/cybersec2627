import psutil

def top_procesos_por_memoria(n: int = 5) -> list[tuple[float, int, str]]:
    procesos = []
    for p in psutil.process_iter(["pid", "name", "memory_percent"]):
        try:
            mem = p.info["memory_percent"] or 0.0
            procesos.append((mem, p.info["pid"], p.info["name"]))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # El proceso murió o no tenemos permiso: lo ignoramos sin romper
            continue
    return sorted(procesos, reverse=True)[:n]

for mem_pct, pid, nombre in top_procesos_por_memoria(3):
    print(f"PID {pid:6}  {nombre:22}  {mem_pct:.1f}% memoria")