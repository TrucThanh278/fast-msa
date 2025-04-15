FROM python:3.10-alpine

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r ./requirements.txt \
    && rm -rf /root/.cache/pip

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]