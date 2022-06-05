from importlib import import_module
import json
import logging
from logging.handlers import RotatingFileHandler
from threading import Thread
import time

from pytwitter import Api
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from wikitransbot.exceptions import (
    ArticleCommandEmptyRequestException,
    InvalidCommandException,
)


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
        self.running = True

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
        self.command_handlers_config = self.config["command_handlers"]

        self.load_handlers()

    def load_handlers(self):
        self.handlers = {}
        for handler_name, handler_config in self.command_handlers_config.items():
            for alias in handler_config["aliases"]:
                module_name = handler_config["module"]
                module = import_module(module_name)
                handler = getattr(module, handler_name)
                self.handlers[alias] = handler

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
            self.logger.exception(f"❗{str(e)}")
            raise e

    def write_since_id(self, file_path: str, since_id: int) -> None:
        with open(file_path, "w") as f:
            f.write(str(since_id))

    def tweet(self, *, text, to):
        self.api.create_tweet(
            text=text,
            reply_in_reply_to_tweet_id=to,
            reply_exclude_reply_user_ids=[],
        )
        self.logger.debug(f"Answer sent to #{to} with message {text}")

    def update_since_id(self, new_since_id: int) -> None:
        self.old_since_id = self.since_id
        self.since_id = max(new_since_id, self.since_id)

    def get_command_handler(self, command_alias: str) -> callable:
        command = self.handlers.get(command_alias)
        if command:
            return command
        else:
            raise InvalidCommandException

    def run(self):
        self.logger.debug("👍 Started.")
        while self.running:
            try:
                self.logger.debug("🔎 Checking for new tweets...")
                tweets = self.api.get_mentions(
                    user_id=self.wikitransbot_id, since_id=self.since_id
                ).data
                for tweet in tweets:
                    self.logger.debug(f"🐦 Tweet received: {tweet.text}")
                    self.update_since_id(int(tweet.id))
                    message = tweet.text.split("@wikitransbot")[1]
                    command_keyword = message.split()[0]
                    request = ' '.join(message.split()[1:])
                    self.logger.debug(f"❕ Command received: {command_keyword}")
                    self.logger.debug(f"🗨️ Request received: {request}")
                    command_handler = (
                        self.get_command_handler(command_keyword)
                        (request=request, stop_words=self.stop_words, logger=self.logger)
                    )
                    answer = command_handler.handle()
                    self.tweet(text=answer, to=tweet.id)

            except InvalidCommandException:
                self.logger.exception(f"⛔ Command {command_keyword} not found.")
            except ArticleCommandEmptyRequestException:
                self.logger.exception(f"🚫 No request found for tweet {tweet.id}")
            except Exception as e:
                self.since_id = self.old_since_id
                self.logger.exception(f"❗{str(e)}")

            self.write_since_id(self.since_id_file_path, self.since_id)
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
