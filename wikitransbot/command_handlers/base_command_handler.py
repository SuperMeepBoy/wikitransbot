import json
import logging


class BaseCommandHandler:

    def __init__(self, *, request: str, stop_words: list, logger: logging.Logger):
        self.request = request
        self.stop_words = stop_words
        self.logger = logger
        self.config = json.load(
            open("/etc/wikitransbot/config.json", "r", encoding="utf-8")
        )["command_handlers"]

    def get_handler_name(self) -> str:
        return self.__class__.__name__

    def handle(self):
        raise NotImplementedError
