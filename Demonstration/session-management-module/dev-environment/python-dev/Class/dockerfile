FROM python:3.8-slim

# Install pkg-config, MySQL development package, and build tools
RUN apt-get update \
    && apt-get install -y pkg-config default-libmysqlclient-dev build-essential

# Install MariaDB development files
RUN apt-get install -y libmariadb-dev

WORKDIR /app
COPY . /app

# Upgrade pip and install requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80
ENV FLASK_DEBUG=1

CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
