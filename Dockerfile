FROM debian:latest

RUN apt-get -y update && apt-get upgrade -y
RUN apt-get install -y python3 python3-dev python3-pip

RUN mkdir /etc/wikitransbot
RUN chmod 755 /etc/wikitransbot

COPY wikitransbot /shared/wikitransbot/wikitransbot
COPY requirements.txt /shared/
COPY setup.py /shared/
COPY config.json /etc/wikitransbot/config.json

WORKDIR /shared
VOLUME ["/shared"]

RUN pip3 install -r requirements.txt
RUN pip install -e .

CMD ["python3", "wikitransbot/wikitransbot/main.py"]
