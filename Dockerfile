FROM debian:latest

RUN apt-get -y update && apt-get upgrade -y
RUN apt-get install -y python3 python3-dev python3-pip

COPY . /shared/

WORKDIR /shared
VOLUME ["/shared"]

RUN pip3 install -r requirements.txt
RUN pip install -e .
