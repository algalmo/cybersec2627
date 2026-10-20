import psutil
import platform

def informe() -> None:
    print("=== INFORME DE AUDITORÍA DEL SISTEMA ===")
    print("SO:", platform.system(), platform.release())
    print("CPU:", psutil.cpu_percent(interval=0.3), "%")

    mem = psutil.virtual_memory()
    print(f"Memoria: {mem.percent}% ({mem.used // (1024**2)} MB / {mem.total // (1024**2)} MB)")

    print("\n-- Procesos visibles (top 5 por memoria) --")
    procesos = []
    for p in psutil.process_iter(["pid", "name", "memory_percent"]):
        try:
            procesos.append((p.info["memory_percent"] or 0.0, p.info["pid"], p.info["name"]))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    for mem_pct, pid, nombre in sorted(procesos, reverse=True)[:5]:
        print(f"  PID {pid:6}  {nombre:22}  {mem_pct:.1f}%")

    print(f"\nTotal de procesos visibles: {len(procesos)}")
    print("(Dentro de un contenedor, estos son los procesos DE ESE contenedor.)")

if __name__ == "__main__":
    informe()
