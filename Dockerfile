FROM python:3.8.10

WORKDIR /code

RUN apt -y update

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /code/src/application/
CMD ["python", "main.py"]
