FROM python:3.12.4-alpine3.20

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
CMD ["python", "app.py"]