# Genera eventos sobre la carpeta vigilada, para la demostración.
import time
from pathlib import Path

carpeta = Path("vigilada")
carpeta.mkdir(exist_ok=True)
time.sleep(1)
(carpeta / "documento.txt").write_text("contenido inicial"); time.sleep(0.5)
(carpeta / "documento.txt").write_text("contenido modificado"); time.sleep(0.5)
(carpeta / "documento.txt").rename(carpeta / "renombrado.txt"); time.sleep(0.5)
(carpeta / "renombrado.txt").unlink()
print("Eventos provocados.")
