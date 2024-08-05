FROM python:3.12.4-alpine3.20

WORKDIR /app
COPY . /app

EXPOSE 8000

# https://github.com/docker-library/rabbitmq/issues/436
RUN apk add --no-cache tzdata
ENV TZ="America/Caracas"

RUN pip install -r requirements.txt --no-cache-dir
CMD ["python", "app.py"]