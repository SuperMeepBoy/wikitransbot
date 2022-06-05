import logging
from random import choice

from wikitransbot.command_handlers.base_command_handler import BaseCommandHandler


class TrombinoscopeCommandHandler(BaseCommandHandler):
    def __init__(self, *, request: str, stop_words: list, logger: logging.Logger):
        super().__init__(request=request, stop_words=stop_words, logger=logger)
        handler_name = self.get_handler_name()
        self.command_config = self.config[handler_name]

    def handle(self):
        self.logger.debug("🧑‍🦱 Trombinoscope requested")
        return choice(self.command_config["answer_template"]) % (self.command_config["link"])
