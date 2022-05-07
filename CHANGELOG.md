**[1.1.2] - ????-??-??**


**Changed**

- No longer use the rest of the tweet if user uses a line break in their request

**Fixed**

- Fixed a bug with tweet parsing

**[1.1.1] - 2022-04-22**


**Added**

- Answer templates are now lists so the bot can pick a template in them to have various answers
- Add a list of stopwords to be removed from users' requests
- Add a filewatch on config to load changes dynamically

**Fixed**

- Bot no longer answers whenever someone says the trigger keyword in an answer. Bot now only answers if tagged with their @ and the keyword next to it

**[1.1.0] - 2022-03-19**


**Added**

- The trigger keyword to start a request can now be detected anywhere in the tweet. The request is made with everything that comes after that word.

**Changed**

- Python library to access Twitter API changed from `tweepy` to `python-twitter`

**Fixed**

- Bot can now reply to reply of other tweets or replies
- Fixed a bug where Tweets were to be replied to multiple times
