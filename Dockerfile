FROM debian:latest

RUN apt-get -y update && apt-get upgrade -y
RUN apt-get install -y python3 python3-dev python3-pip python3-venv
RUN apt-get install -y curl

RUN mkdir /etc/wikitransbot
RUN chmod 755 /etc/wikitransbot

COPY wikitransbot /shared/wikitransbot/wikitransbot
COPY pyproject.toml /shared/wikitransbot
COPY config.json /etc/wikitransbot/config.json

WORKDIR /shared/wikitransbot
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3
ENV PATH="/root/.local/bin:$PATH"
RUN poetry install

CMD ["poetry", "run", "python", "wikitransbot/main.py"]
