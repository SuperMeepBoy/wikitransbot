# wikitransbot
Attempt at making a Twitter bot for Wikitrans.

I am not affliated nor working for Wikitrans. I am just taking a try answering a request made on Twitter to have a bot that would answer with article whenever tagged to do so.

# Getting started

First, copy (or rename) the `config_template.json` to `config.json` and fill in the Twitter related informations with your key, token and secrets.

Once it's done you can run it from your computer or in a docker thanks to the Dockerfile

```
$ docker build -t wikitrans .
$ docker run --name wikitrans -td wikitrans
$ docker exec -it wikitrans /bin/bash
```

Then run the bot

```
$ python3 main.py
```
