FROM python:3.9.9-alpine
WORKDIR /usr/app
COPY requirements.txt .
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps gcc musl-dev
COPY . .
ENV PORT=8000
EXPOSE $PORT
CMD ["python", "app.py"]