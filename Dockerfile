FROM debian:latest

RUN apt-get -y update && apt-get upgrade -y
RUN apt-get install -y python3 python3-dev python3-pip

COPY main.py /shared/
COPY credentials.py /shared/
COPY requirements.txt /shared/

RUN pip3 install -r /shared/requirements.txt

VOLUME ["/shared"]
WORKDIR /shared

ENTRYPOINT ["tail", "-f", "/dev/null"]