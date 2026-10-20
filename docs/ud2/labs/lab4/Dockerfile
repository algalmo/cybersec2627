FROM python:3.12-slim
WORKDIR /app
COPY detectar.py auth.log .
RUN useradd --create-home analista
USER analista
CMD ["python", "detectar.py"]
