from unittest.mock import MagicMock, patch

from wikitransbot.command_handlers.help_command_handler import HelpCommandHandler


class TestHelpCommandHandler:

    @patch.object(HelpCommandHandler, "__init__", lambda x: None)
    def test_handle(self):
        # Given
        help_handler = HelpCommandHandler()
        help_handler.command_config = {
            "answer_template": ["template1 %s"],
            "link": "link",
        }
        help_handler.request = ""
        help_handler.logger = MagicMock()

        # When
        answer = help_handler.handle()

        # Then
        help_handler.logger.debug.assert_called_once()
        assert(answer == "template1 link")
