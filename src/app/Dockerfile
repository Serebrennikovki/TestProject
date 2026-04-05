FROM python:3.11-alpine
LABEL authors="Serebrennikov"

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "main.py"]