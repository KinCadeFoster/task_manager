FROM python:3.12

RUN mkdir /TaskManager

WORKDIR /TaskManager

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "app.main:app", "--workers", "10", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8080"]