FROM python:3.10

WORKDIR /code/

COPY . .
RUN pip install -r /code/requirements.txt