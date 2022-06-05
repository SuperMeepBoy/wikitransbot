from unittest.mock import (
    MagicMock,
    PropertyMock,
    patch,
)
import tempfile

import pytest

from wikitransbot.main import Bot
from wikitransbot.exceptions import InvalidCommandException


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

    @patch.object(Bot, "__init__", lambda x: None)
    @patch.object(Bot, "write_since_id", MagicMock())
    @patch.object(Bot, "tweet", MagicMock())
    @patch.object(Bot, "update_since_id", MagicMock())
    @patch.object(Bot, "get_command_handler")
    def test_run_command_ok(self, m_get_command_handler):
        # Given
        tweet_text = "Hey\n\n @wikitransbot command arg1 arg2\n\nThanks a lot"
        Bot.running = PropertyMock(side_effect=[True, False])
        bot = Bot()
        bot.since_id = 1000
        bot.wikitransbot_id = "1111"
        bot.since_id_file_path = "path"
        bot.sleep_time = 60
        bot.stop_words = ["arg1", "arg3"]
        bot.logger = MagicMock()
        bot.api = MagicMock(
            get_mentions=MagicMock(
                return_value=MagicMock(
                    data=[
                        MagicMock(id=1000, text=tweet_text)
                    ]
                )
            )
        )
        command_handler = MagicMock(return_value=MagicMock(handle=MagicMock(return_value="answer")))
        m_get_command_handler.return_value = command_handler

        # When
        with patch("wikitransbot.main.time.sleep") as m_sleep:
            bot.run()

        # Then
        bot.update_since_id.assert_called_once_with(1000)
        m_get_command_handler.assert_called_once_with("command")
        command_handler.assert_called_once_with(
            request="arg1 arg2 Thanks a lot",
            stop_words=bot.stop_words,
            logger=bot.logger
        )
        bot.tweet.assert_called_once_with(text="answer", to=1000)
        bot.write_since_id.assert_called_once_with('path',  1000)
        m_sleep.assert_called_once_with(bot.sleep_time)

    @pytest.mark.parametrize(
        "tweet_command, expected_command",
        [
            ("map", "map"),
            ("carte", "map"),
            ("help", "help"),
        ]
    )
    def test_get_command_handler(self, tweet_command, expected_command):
        with patch.object(Bot, "__init__", lambda x: None):
            bot = Bot()
            bot.handlers = {
                "map": "map",
                "carte": "map",
                "help": "help",
            }
            assert bot.get_command_handler(tweet_command) == expected_command

    def test_get_command_handler_invalid_command(self):
        with patch.object(Bot, "__init__", lambda x: None):
            bot = Bot()
            bot.handlers = {}
            with pytest.raises(InvalidCommandException):
                bot.get_command_handler("invalid")
