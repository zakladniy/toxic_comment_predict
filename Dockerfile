FROM python:3.9.6

WORKDIR /code

RUN apt -y update

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /code/src/application/
CMD ["uvicorn src.application.main:app"]
