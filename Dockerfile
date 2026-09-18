FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask qrcode[pil]

COPY demo_server.py .

EXPOSE 8080

CMD ["python3", "demo_server.py", "--port", "8080"]
