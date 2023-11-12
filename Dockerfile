FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/* .

CMD ["uvicorn", "--host", "0.0.0.0", "main:app"]