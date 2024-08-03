FROM python:3.12.4-alpine3.20

WORKDIR /app
COPY . /app

EXPOSE 8000
RUN pip install -r requirements.txt --no-cache-dir
CMD ["python", "app.py"]