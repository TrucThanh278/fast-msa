FROM python:3.10-alpine


COPY ./requirements.txt ./requirements.txt

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip

RUN pip install -r ./requirements.txt \
    && rm -rf /root/.cache/pip

EXPOSE 8000

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]