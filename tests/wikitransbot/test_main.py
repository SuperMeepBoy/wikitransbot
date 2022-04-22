from unittest.mock import (
    MagicMock,
    patch,
)
import tempfile

import pytest

from wikitransbot.main import Bot


class TestBot:
    def test_get_since_id_ok(self):
        with patch.object(Bot, "__init__", lambda x: None):
            with tempfile.NamedTemporaryFile() as tmp_file:
                bot = Bot()
                bot.since_id_file_path = tmp_file.name
                tmp_file.write(b"1000")
                tmp_file.flush()
                assert bot.get_since_id() == 1000

    def test_get_since_id_nok(self):
        with patch.object(Bot, "__init__", lambda x: None):
            with pytest.raises(FileNotFoundError):
                bot = Bot()
                bot.logger = MagicMock()
                bot.since_id_file_path = ""
                bot.get_since_id()

    @pytest.mark.parametrize(
        "tweet_text, keyword, expected_result",
        [
            (
                "@wikitransbot article féminiser sa voix",
                "article",
                (
                    "https://wikitrans.co/wp-admin/admin-ajax.php?"
                    "action=jet_ajax_search&search_taxonomy%5D=&data%5Bvalue%5D=féminiser voix"
                ),
            ),
            (
                "@ally @wikitransbot article psy transfriendly",
                "article",
                (
                    "https://wikitrans.co/wp-admin/admin-ajax.php?"
                    "action=jet_ajax_search&search_taxonomy%5D=&data%5Bvalue%5D=psy transfriendly"
                ),
            ),
            (
                "@wikitransbot tu as perdu",
                "article",
                "",
            ),
            (
                "@wikitransbot je t'invoque article féminiser sa voix",
                "article",
                "",
            ),
        ],
    )
    def test_build_search_article_url(self, tweet_text, keyword, expected_result):
        with patch.object(Bot, "__init__", lambda x: None):
            bot = Bot()
            bot.keyword = keyword
            bot.stop_words = ["unused_word", "sa"]
            result = bot.build_search_article_url(tweet_text=tweet_text)
            assert result == expected_result
