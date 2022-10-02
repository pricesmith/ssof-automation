FROM alpine:3.16.2

# install packages related to the base build
RUN apk add --no-cache \
	py3-pip \
	python3-dev \
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


# Install the requirements
COPY requirements.txt /opt/app/
RUN pip3 install --no-cache-dir -r /opt/app/requirements.txt

# install app into the app-propriate place :D
COPY . /opt/app/

ENTRYPOINT ["/opt/app/entrypoint.py"]
