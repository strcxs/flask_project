FROM python:3.9-slim-buster
WORKDIR /app

COPY requirements.txt requirements.txt
RUN python3.9 -m pip install -r requirements.txt

COPY /app .

CMD ["flask", "--app", ".", "--debug", "run", "--host=0.0.0.0"]