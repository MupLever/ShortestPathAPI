FROM python:3.8

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

RUN cd app && alembic upgrade head && cd ../

CMD ["gunicorn", "main:app" "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
