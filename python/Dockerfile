FROM mcr.microsoft.com/playwright/python:v1.57.0-jammy

WORKDIR /app

COPY python/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY python/ .

CMD ["python", "parse_nac.py"]
