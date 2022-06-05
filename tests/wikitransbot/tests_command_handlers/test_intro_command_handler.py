from unittest.mock import MagicMock, patch

from wikitransbot.command_handlers.intro_command_handler import IntroCommandHandler


class TestIntroCommandHandler:

    @patch.object(IntroCommandHandler, "__init__", lambda x: None)
    def test_handle(self):
        # Given
        intro_handler = IntroCommandHandler()
        intro_handler.command_config = {
            "answer_template": ["template1 %s"],
            "link": "link",
        }
        intro_handler.request = ""
        intro_handler.logger = MagicMock()

        # When
        answer = intro_handler.handle()

        # Then
        intro_handler.logger.debug.assert_called_once()
        assert(answer == "template1 link")
