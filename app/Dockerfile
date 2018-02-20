FROM python:3.6

WORKDIR /

COPY app.py /
COPY validation/ /validation
COPY requirements.txt /
COPY postgresql/ /postgresql

RUN pip install -r requirements.txt

EXPOSE 80

CMD python app.py
