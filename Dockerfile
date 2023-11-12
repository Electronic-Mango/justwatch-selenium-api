FROM python:3.11-slim

WORKDIR /app

RUN apt update
RUN apt install -y firefox-esr
ENV FIREFOX_BIN="$(which firefox)"
COPY geckodriver* .
ENV FIREFOX_DRIVER="/app/geckodriver"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/* .

CMD ["uvicorn", "--host", "0.0.0.0", "main:app"]
