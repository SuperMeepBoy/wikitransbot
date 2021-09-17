# wikitransbot
Attempt at making a Twitter bot for Wikitrans.

I am not affliated nor working for Wikitrans. I am just taking a try answering a request made on Twitter to have a bot that would answer with article whenever tagged to do so.

# Getting started

In order to get started you first need to install requirements :
```
$ pip install -r requirements.txt
```

In a second time you must create a file named `credentials.py` at the root of this project containing your API key, key secret, access token and access token secret. Remember not to share them with anyone. The file must look somehting like :

```python
TWITTER_API_KEY=<your_twitter_api_key>
TWITTER_API_KEY_SECRET=<your_twitter_api_secret>
TWITTER_ACCESS_TOKEN=<your_twitter_access_token>
TWITTER_ACCESS_TOKEN_SECRET=<your_twitter_access_token_secret>
```

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
