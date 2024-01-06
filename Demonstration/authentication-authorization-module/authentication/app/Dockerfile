FROM python:3.8
WORKDIR /app
COPY . /app

RUN pip install flask
RUN pip install flask_restful
RUN pip install mysql-connector-python
RUN pip install flask-mysqldb
RUN pip install pyotp
RUN pip install pycrypto
RUN pip install pycryptodome
RUN pip install cryptography
RUN pip install PyJWT


EXPOSE 2000
ENTRYPOINT ["python3"]
CMD ["./app.py"]