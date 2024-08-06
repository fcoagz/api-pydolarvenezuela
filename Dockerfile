FROM python:3.12.4-alpine3.20

WORKDIR /app
COPY . /app

EXPOSE 8000

# https://gitlab.alpinelinux.org/alpine/aports/-/issues/12057
ENV TZ="America/Caracas"
RUN apk add --no-cache tzdata
RUN ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime

RUN pip install -r requirements.txt --no-cache-dir
CMD ["python", "app.py"]