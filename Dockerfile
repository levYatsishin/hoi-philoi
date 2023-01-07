FROM python:3.10

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY app app
COPY db_api db_api
COPY main.py main.py

CMD ["python3", "main.py"]