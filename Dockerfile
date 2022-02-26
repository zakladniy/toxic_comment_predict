FROM python:3.9.6-buster

WORKDIR /code

RUN apt -y update

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "src.application.main:app", "--host", "0.0.0.0", "--port", "80"]
