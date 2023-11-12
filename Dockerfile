FROM python:3.11-alpine

WORKDIR /app

RUN apk update
RUN apk add gcc musl-dev libffi-dev firefox
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY geckodriver* .
ENV FIREFOX_BIN="$(which firefox)"
ENV FIREFOX_DRIVER="/app/geckodriver"
COPY src/* .

CMD ["uvicorn", "--host", "0.0.0.0", "main:app"]
