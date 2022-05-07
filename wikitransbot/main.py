import json
import logging
from logging.handlers import RotatingFileHandler
from random import choice
from threading import Thread
import time

from pytwitter import Api
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .cmd import (
    Cmd,
    CmdNotFound,
    InvalidCmd,
    SearchFailed,
    SearchNotFound,
)


class InvalidTweet(ValueError):
    def __init__(self):
        super(InvalidTweet, self).__init__("Invlaid Tweet.")


class ConfigWatcher:
    watched_file = "/etc/wikitransbot/config.json"

    def __init__(self, bot):
        self.observer = Observer()
        self.bot = bot

    def run(self):
        event_handler = ConfigHandler(self.bot)
        self.observer.schedule(event_handler, self.watched_file)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except Exception:
            self.observer.stop()

        self.observer.join()


class ConfigHandler(FileSystemEventHandler):
    def __init__(self, bot):
        self.bot = bot

    def on_modified(self, event):
        if event.event_type == "modified":
            self.bot.load_config()


class Bot:
    def __init__(self):
        self.load_config()

    def load_config(self):
        self.config = json.load(
            open("/etc/wikitransbot/config.json", "r", encoding="utf-8")
        )

        # Logger
        logfile = self.config["logfile_path"]
        logging.basicConfig(
            filename=logfile,
            filemode="a",
            level=logging.DEBUG,
            format="[%(levelname)s] %(asctime)s:%(message)s",
        )
        self.logger = logging.getLogger()
        handler = RotatingFileHandler(logfile, maxBytes=10 * 1024 * 1024, backupCount=1)
        self.logger.addHandler(handler)

        # Bot related variables
        self.api = self.get_twitter_api()
        self.wikitransbot_id = self.config["twitter"]["user_id"]
        self.old_since_id = 1
        self.since_id_file_path = self.config["last_id_file"]
        self.since_id = self.get_since_id()
        self.stop_words = self.config["stop_words"]
        self.sleep_time = self.config["sleep_time"]

    def get_twitter_api(self):
        twitter_config = self.config["twitter"]
        return Api(
            consumer_key=twitter_config["twitter_api_key"],
            consumer_secret=twitter_config["twitter_api_key_secret"],
            access_token=twitter_config["twitter_access_token"],
            access_secret=twitter_config["twitter_access_token_secret"],
        )

    def get_since_id(self):
        try:
            with open(self.since_id_file_path, "r") as f:
                return int(f.read())
        except FileNotFoundError as e:
            self.logger.error(str(e))
            raise e

    def tweet(self, *, text, to):
        self.api.create_tweet(
            text=text,
            reply_in_reply_to_tweet_id=to,
            reply_exclude_reply_user_ids=[],
        )
        self.logger.info(f"Answer sent to #{to} with message {text}")

    def update_since_id(self, new_since_id):
        self.old_since_id = self.since_id
        self.since_id = max(new_since_id, self.since_id)

    def run(self):
        cmd = Cmd(self.stop_words)

        while True:
            try:
                tweets = self.api.get_mentions(
                    user_id=self.wikitransbot_id, since_id=self.since_id
                ).data
                for tweet in tweets:
                    try:
                        self.update_since_id(int(tweet.id))
                        msg = cmd.exec(tweet.text)
                        answer_template = choice(self.config["answer_template"])
                        self.tweet(
                            text=answer_template % (msg),
                            to=tweet.id,
                        )
                    except SearchNotFound:
                        no_answer_template = choice(self.config["no_answer_template"])
                        self.tweet(text=no_answer_template, to=tweet.id)
                    except SearchFailed:
                        # network issues re-try ?
                        continue
                    except CmdNotFound:
                        # tweet a default command or a help message
                        continue
                    except InvalidCmd:
                        # tweet the command help
                        continue
            except Exception as e:
                self.since_id = self.old_since_id
                self.logger.warning(str(e))

            with open(self.since_id_file_path, "w") as f:
                f.write(
                    str(self.since_id)
                )  # So if the bot crashes we know where to start

            time.sleep(self.sleep_time)


if __name__ == "__main__":
    bot = Bot()
    bot_thread = Thread(target=bot.run)

    config_watcher = ConfigWatcher(bot)
    config_watcher_thread = Thread(target=config_watcher.run)

    bot_thread.start()
    config_watcher_thread.start()
    bot_thread.join()
    config_watcher_thread.join()
