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
