from unittest.mock import MagicMock, patch

import pytest

from wikitransbot.command_handlers.article_command_handler import ArticleCommandHandler
from wikitransbot.exceptions import ArticleCommandEmptyRequestException


class TestArticleCommandHandler:

    @patch.object(ArticleCommandHandler, "__init__", lambda x: None)
    def test_get_clean_request(self):
        # Given
        article_handler = ArticleCommandHandler()
        article_handler.request = "féminiser sa voix & visage\n\n\rMerci"
        article_handler.stop_words = ["et", "sa", "mon"]

        # When
        clean_request = article_handler.get_clean_request()

        # Then
        assert(clean_request == "féminiser voix & visage")

    @patch.object(ArticleCommandHandler, "__init__", lambda x: None)
    def test_build_search_article_url(self):
        # Given
        article_handler = ArticleCommandHandler()
        clean_request = "féminiser voix & visage"

        # When
        article_url = article_handler.build_search_article_url(clean_request=clean_request)

        # Then
        assert(
            article_url ==
            "https://wikitrans.co/wp-admin/admin-ajax.php"
            "?action=jet_ajax_search&search_taxonomy%5D=&data%5Bvalue%5D=f%C3%A9miniser%20voix%20%26%20visage"
        )

    @patch.object(ArticleCommandHandler, "__init__", lambda x: None)
    @patch.object(ArticleCommandHandler, "get_clean_request", MagicMock(return_value="request"))
    @patch.object(ArticleCommandHandler, "build_search_article_url", MagicMock(return_value="search_article_url"))
    @patch("wikitransbot.command_handlers.article_command_handler.requests.get")
    def test_handle(self, m_requests):
        # Given
        article_handler = ArticleCommandHandler()
        article_handler.command_config = {
            "answer_template": ["template1 %s"],
        }
        article_handler.request = "request"
        article_handler.logger = MagicMock()
        m_requests.return_value = MagicMock(
            status_code=200,
            json=MagicMock(
                return_value={
                    "data": {
                        "post_count": 1,
                        "posts": [{"link": "url/article/"}],
                    }
                }
            ),
        )

        # When
        answer = article_handler.handle()

        # Then
        assert(article_handler.logger.debug.call_count == 2)
        assert(answer == "template1 url/article/")

    @patch.object(ArticleCommandHandler, "__init__", lambda x: None)
    @patch.object(ArticleCommandHandler, "get_clean_request", MagicMock(return_value="request"))
    @patch.object(ArticleCommandHandler, "build_search_article_url", MagicMock(return_value="search_article_url"))
    @patch("wikitransbot.command_handlers.article_command_handler.requests.get")
    def test_handle_no_article(self, m_requests):
        # Given
        article_handler = ArticleCommandHandler()
        article_handler.command_config = {
            "no_answer_template": ["no answer"],
        }
        article_handler.request = "request"
        article_handler.logger = MagicMock()
        m_requests.return_value = MagicMock(
            status_code=200,
            json=MagicMock(
                return_value={
                    "data": {
                        "post_count": 0,
                        "posts": [],
                    }
                }
            ),
        )

        # When
        answer = article_handler.handle()

        # Then
        assert(article_handler.logger.debug.call_count == 2)
        assert(answer == "no answer")

    @patch.object(ArticleCommandHandler, "__init__", lambda x: None)
    @patch.object(ArticleCommandHandler, "get_clean_request", MagicMock(return_value="request"))
    @patch.object(ArticleCommandHandler, "build_search_article_url", MagicMock(return_value="search_article_url"))
    @patch("wikitransbot.command_handlers.article_command_handler.requests.get")
    def test_handle_issue(self, m_requests):
        # Given
        article_handler = ArticleCommandHandler()
        article_handler.command_config = {
            "issue_template": ["an issue occured"],
        }
        article_handler.request = "request"
        article_handler.logger = MagicMock()
        m_requests.return_value = MagicMock(
            status_code=500,
        )

        # When
        answer = article_handler.handle()

        # Then
        assert(article_handler.logger.debug.call_count == 2)
        assert(answer == "an issue occured")

    @patch.object(ArticleCommandHandler, "__init__", lambda x: None)
    @patch("wikitransbot.command_handlers.article_command_handler.requests.get")
    def test_handle_empty_request(self, m_requests):
        # Given
        article_handler = ArticleCommandHandler()
        article_handler.request = ""
        article_handler.logger = MagicMock()
        m_requests.return_value = MagicMock(
            status_code=500,
        )

        with pytest.raises(ArticleCommandEmptyRequestException):
            article_handler.handle()

        assert(article_handler.logger.debug.call_count == 1)
