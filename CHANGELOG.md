**[1.1.1] - 2022-04-22**

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
