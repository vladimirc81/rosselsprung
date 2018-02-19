FROM python:3.6

WORKDIR /

COPY app.py /
COPY validation/ /validation
COPY requirements.txt /
COPY postgresql/ /postgresql
COPY rates.sql /

RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y postgresql-client

EXPOSE 80

CMD python app.py
