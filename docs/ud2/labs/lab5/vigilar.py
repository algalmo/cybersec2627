import sys
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Vigilante(FileSystemEventHandler):
    def _marca(self, tipo: str, ruta: str) -> None:
        print(f"{time.strftime('%H:%M:%S')}  [{tipo:11}] {ruta}", flush=True)

    def on_created(self, event):
        if not event.is_directory:
            self._marca("CREADO", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self._marca("MODIFICADO", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self._marca("BORRADO", event.src_path)

    def on_moved(self, event):
        self._marca("RENOMBRADO", f"{event.src_path} -> {event.dest_path}")

def vigilar(carpeta: str, segundos: int) -> None:
    Path(carpeta).mkdir(parents=True, exist_ok=True)
    observador = Observer()
    observador.schedule(Vigilante(), carpeta)
    observador.start()
    print(f"Vigilando '{carpeta}' durante {segundos}s...", flush=True)
    try:
        time.sleep(segundos)
    finally:
        observador.stop()
        observador.join()
    print("Vigilancia terminada.", flush=True)

if __name__ == "__main__":
    carpeta = sys.argv[1] if len(sys.argv) > 1 else "vigilada"
    segundos = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    vigilar(carpeta, segundos)
