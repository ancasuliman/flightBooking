FROM python:3.6

EXPOSE 5000

WORKDIR /server

COPY requirements.txt /server
RUN pip install -r requirements.txt

COPY app.py /server
CMD python app.py
