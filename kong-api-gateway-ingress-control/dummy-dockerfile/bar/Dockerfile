FROM python:3-alpine

WORKDIR /app

RUN pip install flask
COPY bar.py .

EXPOSE 5000

CMD ["python", "bar.py"]