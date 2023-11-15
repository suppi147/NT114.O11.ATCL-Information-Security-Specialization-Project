FROM python:3-alpine

WORKDIR /app

RUN pip install flask
COPY foo.py .

EXPOSE 5000

CMD ["python", "foo.py"]