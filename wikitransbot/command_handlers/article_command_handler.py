import logging
from random import choice
import re
import requests
import urllib.parse

from wikitransbot.command_handlers.base_command_handler import BaseCommandHandler
from wikitransbot.exceptions import ArticleCommandEmptyRequestException


class ArticleCommandHandler(BaseCommandHandler):
    def __init__(self, *, request: str, stop_words: list, logger: logging.Logger):
        super().__init__(request=request, stop_words=stop_words, logger=logger)
        handler_name = self.get_handler_name()
        self.command_config = self.config[handler_name]

    def get_clean_request(self) -> str:
        return " ".join(
            [
                word.lower()
                for word in re.split("[\n\r]", self.request)[0].split()
                if word.lower() not in self.stop_words
            ]
        )

    def build_search_article_url(self, *, clean_request) -> str:
        base_url = "https://wikitrans.co/wp-admin/admin-ajax.php"
        parameters = "?action=jet_ajax_search&search_taxonomy%5D=&data%5Bvalue%5D="
        url = base_url + parameters
        return f"{url}{urllib.parse.quote(clean_request)}"

    def handle(self):
        self.logger.debug("📰 Article requested")
        if not self.request:
            raise ArticleCommandEmptyRequestException
        clean_request = self.get_clean_request()
        search_article_url = self.build_search_article_url(clean_request=clean_request)

        self.logger.debug(f"🔗 Looking for article on link {search_article_url}")
        response = requests.get(search_article_url)
        if response.status_code == 200:
            data = response.json()["data"]
            if not data["post_count"]:
                return choice(self.command_config["no_answer_template"])
            else:
                answer_template = choice(self.command_config["answer_template"])
                return answer_template % (data["posts"][0]["link"])
        else:
            return choice(self.command_config["issue_template"])
