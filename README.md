# wikitransbot
Attempt at making a Twitter bot for Wikitrans.

I am not affliated nor working for Wikitrans. I am just taking a try answering a request made on Twitter to have a bot that would answer with article whenever tagged to do so.

# Getting started

In order to get started you first need to install requirements :
```
$ pip install -r requirements.txt
```

In a second time you must fill the config file. Copy (or rename) the `config_template.json` to `config.json` and fill in the Twitter related informations with your keys and token.

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
