from unittest.mock import (
    MagicMock,
    patch,
)
import tempfile

import pytest

from wikitransbot.main import Bot, InvalidTweet


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
            ("@wikitransbot article féminiser sa voix", "article", "féminiser voix"),
            (
                "@ally @wikitransbot article psy transfriendly",
                "article",
                "psy transfriendly",
            ),
            (
                "@wikitransbot article féminiser voix & visage",
                "article",
                "féminiser voix & visage",
            ),
            (
                "Hey, check it out!\n@wikitransbot article féminiser sa voix\nAwesome article!",
                "article",
                "féminiser voix",
            ),
        ],
    )
    def test_clean_tweet_text(self, tweet_text, keyword, expected_result):
        with patch.object(Bot, "__init__", lambda x: None):
            bot = Bot()
            bot.keyword = keyword
            bot.stop_words = ["unused_word", "sa"]
            result = bot.clean_tweet_text(tweet_text=tweet_text)
            assert result == expected_result

    @pytest.mark.parametrize(
        "tweet_text, keyword, expected_result",
        [
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
    def test_clean_tweet_text_raise_invalid_tweet(
        self, tweet_text, keyword, expected_result
    ):
        with patch.object(Bot, "__init__", lambda x: None):
            bot = Bot()
            bot.keyword = keyword
            bot.stop_words = []
            with pytest.raises(InvalidTweet):
                bot.clean_tweet_text(tweet_text=tweet_text)

    @pytest.mark.parametrize(
        "m_clean_tweet_text_return_value, expected_result",
        [
            (
                "féminiser voix",
                "https://wikitrans.co/wp-admin/admin-ajax.php"
                "?action=jet_ajax_search&search_taxonomy%5D=&data%5Bvalue%5D=f%C3%A9miniser%20voix",
            ),
            (
                "féminiser voix & visage",
                "https://wikitrans.co/wp-admin/admin-ajax.php"
                "?action=jet_ajax_search&search_taxonomy%5D=&data%5Bvalue%5D=f%C3%A9miniser%20voix%20%26%20visage",
            ),
            (
                InvalidTweet(),
                "",
            ),
        ],
    )
    @patch.object(Bot, "clean_tweet_text")
    def test_build_search_article_url(
        self, m_clean_tweet_text, m_clean_tweet_text_return_value, expected_result
    ):
        m_clean_tweet_text.side_effect = [m_clean_tweet_text_return_value]
        with patch.object(Bot, "__init__", lambda x: None):
            bot = Bot()
            result = bot.build_search_article_url(tweet_text="w/e")
            assert result == expected_result
