FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY vigilar.py provocar.py .
RUN useradd --create-home vigilante && mkdir -p /app/vigilada && chown -R vigilante /app
USER vigilante
CMD ["sh", "-c", "python vigilar.py vigilada 8 & sleep 1 && python provocar.py && wait"]
