FROM python:latest

WORKDIR /server

ADD ./server /server
ADD ./requirements.txt /server
ADD ./.env /server


RUN pip install -r requirements.txt

CMD ["python", "main.py"]
