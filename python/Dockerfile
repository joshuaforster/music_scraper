FROM mcr.microsoft.com/playwright/python:v1.49.1-jammy

WORKDIR /app

COPY python/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY python/ .

CMD ["python", "parse_nac.py"]
