FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY auditor.py .
RUN useradd --create-home auditor
USER auditor
CMD ["python", "auditor.py"]
