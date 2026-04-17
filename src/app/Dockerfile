FROM python:3.11-alpine
LABEL authors="Serebrennikov"

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "api.py"]