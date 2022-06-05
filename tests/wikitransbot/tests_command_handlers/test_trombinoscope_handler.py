from unittest.mock import MagicMock, patch

from wikitransbot.command_handlers.trombinoscope_command_handler import TrombinoscopeCommandHandler


class TestTrombinoscopeCommandHandler:

    @patch.object(TrombinoscopeCommandHandler, "__init__", lambda x: None)
    def test_handle(self):
        # Given
        trombinoscope_handler = TrombinoscopeCommandHandler()
        trombinoscope_handler.command_config = {
            "answer_template": ["template1 %s"],
            "link": "link",
        }
        trombinoscope_handler.request = ""
        trombinoscope_handler.logger = MagicMock()

        # When
        answer = trombinoscope_handler.handle()

        # Then
        trombinoscope_handler.logger.debug.assert_called_once()
        assert(answer == "template1 link")
