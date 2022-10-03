FROM alpine:3.16.2

# ARG PYTHON_VERSION=3.10.7

# RUN apk add --no-cache \
# 	wget \
# 	gcc \
# 	make \
# 	zlib-dev \
# 	libffi-dev \
# 	openssl-dev \
# 	musl-dev

# install packages related to the base build
RUN apk add --no-cache \
	py3-pip \
	python3-dev \
	&& :

# Install Airflow dependencies and tools
RUN apk add --no-cache \
    wget \
    gcc \
    g++ \
    zlib-dev \
    libffi-dev \
    openssl-dev \
    musl-dev \
    git \
    inetutils-telnet \
    freetds-dev \
	libpq-dev \
    rsync \
    zip \
    unzip \
    vim \
    && :

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
ARG AIRFLOW_HOME=/opt/app

# Export the environment variable AIRFLOW_HOME where airflow will be installed
ENV AIRFLOW_HOME=${AIRFLOW_HOME}

# Install the requirements
COPY requirements.txt /opt/app/
RUN pip3 install --no-cache-dir -r /opt/app/requirements.txt

# install app into the app-propriate place :D
COPY . /opt/app/

ENTRYPOINT ["/opt/app/entrypoint.py"]
