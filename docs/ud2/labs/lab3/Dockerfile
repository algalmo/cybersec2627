FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY generar_pcap.py analizar.py .
RUN useradd --create-home analista && chown analista /app
USER analista
CMD ["sh", "-c", "python generar_pcap.py && python analizar.py"]
