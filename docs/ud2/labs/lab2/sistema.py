import psutil
import platform

print("Sistema operativo:", platform.system(), platform.release())
print("Uso de CPU:", psutil.cpu_percent(interval=0.3), "%")

mem = psutil.virtual_memory()
print(f"Memoria: {mem.percent}% usada "
      f"({mem.used // (1024**2)} MB de {mem.total // (1024**2)} MB)")
