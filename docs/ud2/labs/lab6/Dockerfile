FROM python:3.12-slim
WORKDIR /app
COPY correlacionar.py .
RUN useradd --create-home defensa && chown defensa /app
USER defensa
CMD ["python", "correlacionar.py"]
