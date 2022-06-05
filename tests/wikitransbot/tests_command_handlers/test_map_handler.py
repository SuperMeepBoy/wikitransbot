from unittest.mock import MagicMock, patch

from wikitransbot.command_handlers.map_command_handler import MapCommandHandler


class TestMapCommandHandler:

    @patch.object(MapCommandHandler, "__init__", lambda x: None)
    def test_handle(self):
        # Given
        map_handler = MapCommandHandler()
        map_handler.command_config = {
            "answer_template": ["template1 %s"],
            "link": "link",
        }
        map_handler.request = ""
        map_handler.logger = MagicMock()

        # When
        answer = map_handler.handle()

        # Then
        map_handler.logger.debug.assert_called_once()
        assert(answer == "template1 link")
