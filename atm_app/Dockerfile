FROM python:3.8-slim-buster

WORKDIR /home

COPY . /home

RUN pip install -r requirements.txt

ENV ENV=test

CMD ["python", "main.py"]