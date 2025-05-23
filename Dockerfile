FROM python:3.12-alpine
ENV TZ='UTC'

RUN apk add --no-cache tzdata

WORKDIR /app/src

COPY requirements.txt ./requirements.txt

RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt && \
    apk del .build-deps


COPY ./src/ ./src/

CMD ["python", "src/main.py"]
