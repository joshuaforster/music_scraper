FROM mcr.microsoft.com/playwright/python:v1.49.1-jammy

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps chromium

COPY . .

CMD ["python3", "parse_nac.py"]
