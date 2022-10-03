FROM alpine:3.16.2

# install packages related to the base build
RUN apk add --no-cache \
	py3-pip \
	python3-dev \
	&& :

# Install Airflow dependencies and tools
RUN apt-get update -yqq && \
    apt-get upgrade -yqq && \
    apt-get install -yqq --no-install-recommends \ 
    wget \
    libczmq-dev \
    curl \
    libssl-dev \
    git \
    inetutils-telnet \
    bind9utils freetds-dev \
    libkrb5-dev \
    libsasl2-dev \
    libffi-dev libpq-dev \
    freetds-bin build-essential \
    default-libmysqlclient-dev \
    apt-utils \
    rsync \
    zip \
    unzip \
    gcc \
    vim \
    locales \
    && apt-get clean

# install packages specifically related to network troubleshooting
RUN apk add --no-cache \
	-X http://dl-cdn.alpinelinux.org/alpine/edge/main \
	-X http://dl-cdn.alpinelinux.org/alpine/edge/community \
	-X http://dl-cdn.alpinelinux.org/alpine/edge/testing \
	bash \
	bind-tools \
	curl \
	fping \
	hping3 \
	iproute2 \
	iproute2-minimal \
	iproute2-ss \
	mtr \
	openssl \
	traceroute \
	&& :

# Airflow build and setup Args
ARG AIRFLOW_VERSION=2.4.1
ARG AIRFLOW_HOME=/opt/airflow

# Export the environment variable AIRFLOW_HOME where airflow will be installed
ENV AIRFLOW_HOME=${AIRFLOW_HOME}

# Install the requirements
RUN PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
RUN wget https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt
COPY constraints.txt /opt/app/
RUN pip3 install apache-airflow[celery, docker] --no-cache-dir -r /opt/app/constraints.txt

# install app into the app-propriate place :D
COPY . /opt/app/

ENTRYPOINT ["/opt/app/entrypoint.py"]
