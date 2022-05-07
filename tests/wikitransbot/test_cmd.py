from unittest.mock import (
    patch,
)

import pytest

from wikitransbot.cmd import (
    Article,
    Cmd,
    CmdNotFound,
    Intro,
    InvalidCmd,
    SearchFailed,
    SearchNotFound,
)


class FakeCmd:

    def match(self, cmd_name):
        raise NotImplementedError

    def do(self, search):
        raise NotImplementedError

    def help(self):
        raise NotImplementedError


class TestCmd:

    @pytest.mark.parametrize(
        "tweet_text, expected_cmd",
        [
            (
                "@wikitransbot tu as perdu",
                "tu",
            ),
            (
                "@wikitransbot je t'invoque article féminiser sa voix",
                "je",
            ),
            (
                "article @wikitransbot féminiser",
                "féminiser",
            ),
        ]
    )
    def test_exec_cmd_not_found(self, tweet_text, expected_cmd):
        with patch('wikitransbot.cmd.CmdBase.__subclasses__') as mock_cmd:
            with patch.object(FakeCmd, 'match', return_value=False) as fake_cmd:
                mock_cmd.return_value = [FakeCmd]

                with pytest.raises(CmdNotFound):
                    Cmd(["unused_word", "sa"]).exec(tweet_text)

                fake_cmd.assert_called_once_with(expected_cmd)

    @pytest.mark.parametrize(
        "tweet_text",
        [
            "@wikitransbot",
            "article @wikitransbot",
        ]
    )
    def test_exec_cmd_no_cmd(self, tweet_text):
        with patch('wikitransbot.cmd.CmdBase.__subclasses__') as mock_cmd:
            with patch.object(FakeCmd, 'match', return_value=False) as fake_cmd:
                mock_cmd.return_value = [FakeCmd]

                with pytest.raises(CmdNotFound):
                    Cmd(["unused_word", "sa"]).exec(tweet_text)

                fake_cmd.assert_not_called()

    @pytest.mark.parametrize(
        "tweet_text, expected_cmd, expected_search",
        [
            (
                "@wikitransbot article féminiser sa voix",
                "article",
                "féminiser voix"
            ),
            (
                "@ally @wikitransbot article psy transfriendly",
                "article",
                "psy transfriendly",
            ),
            (
                "@wikitransbot article test & féminiser",
                "article",
                "test & féminiser",
            ),
            (
                "Salut je veux trouver un article sur le wikitrans\n@wikitransbot article mon article\n merci beacoup",
                "article",
                "mon article",
            ),
        ]
    )
    def test_exec_cmd_do(self, tweet_text, expected_cmd, expected_search):
        with patch('wikitransbot.cmd.CmdBase.__subclasses__') as mock_cmd:
            with patch.object(FakeCmd, 'match', return_value=True) as fake_match:
                with patch.object(FakeCmd, 'do', return_value="un très bon article") as fake_do:
                    mock_cmd.return_value = [FakeCmd]

                    result = Cmd(["unused_word", "sa"]).exec(tweet_text)
                    fake_match.assert_called_once_with(expected_cmd)
                    fake_do.assert_called_once_with(expected_search)
                    assert result == "un très bon article"


class TestArticle:

    @pytest.mark.parametrize(
        "tweet_text, expected_search",
        [
            (
                "féminiser voix",
                (
                    "https://wikitrans.co/wp-admin/admin-ajax.php?"
                    "action=jet_ajax_search&search_taxonomy%5D=&data%5Bvalue%5D=f%C3%A9miniser%20voix"
                ),
            ),
            (
                "psy transfriendly",
                (
                    "https://wikitrans.co/wp-admin/admin-ajax.php?"
                    "action=jet_ajax_search&search_taxonomy%5D=&data%5Bvalue%5D=psy%20transfriendly"
                ),
            ),
            (
                "test & féminiser",
                (
                        "https://wikitrans.co/wp-admin/admin-ajax.php?"
                        "action=jet_ajax_search&search_taxonomy%5D=&data%5Bvalue%5D=test%20%26%20f%C3%A9miniser"
                ),
            ),
        ],
    )
    def test_do_valid(self, tweet_text, expected_search):
        with patch('requests.get') as mock_request:
            expected_result = 'linked found'

            mock_request.return_value.status_code = 200
            mock_request.return_value.json = lambda: {
                "data": {
                    "post_count": 1,
                    "posts": [
                        {
                            "link": expected_result,
                        },
                    ],
                },
            }

            result = Article().do(tweet_text)
            mock_request.assert_called_once_with(expected_search)
            assert result == expected_result

    def test_do_not_found(self):
        with patch('requests.get') as mock_request:
            mock_request.return_value.status_code = 200
            mock_request.return_value.json = lambda: {
                "data": {
                    "post_count": 0,
                },
            }

            with pytest.raises(SearchNotFound):
                Article().do("féminiser voix")

    @pytest.mark.parametrize(
        "tweet_text",
        [
            None,
            "",
        ]
    )
    def test_do_invalid(self, tweet_text):
        with pytest.raises(InvalidCmd):
            Article().do(tweet_text)

    def test_do_failed(self):
        with patch('requests.get') as mock_request:
            mock_request.return_value.status_code = 500

            with pytest.raises(SearchFailed):
                Article().do("féminiser voix")

    @pytest.mark.parametrize(
        "cmd_name, expected_result",
        [
            (
                "article", True,
            ),
            (
                "bad", False,
            ),
            (
                "", False,
            ),
            (
                None, False,
            ),
        ],
    )
    def test_match(self, cmd_name, expected_result):
        result = Article().match(cmd_name)
        assert result == expected_result

    def test_help(self):
        assert Article().help() == "@wikitransbot article recherche"


class TestIntro:

    @pytest.mark.parametrize(
        "search",
        [
            "",
            None,
            "some other keyword",
        ]
    )
    def test_do(self, search):
        assert Intro().do(search) == "https://wikitrans.co/intro/"

    @pytest.mark.parametrize(
        "cmd_name, expected_result",
        [
            (
                "intro", True,
            ),
            (
                "transidentité", True,
            ),
            (
                "transidentite", True,
            ),
            (
                "bad", False,
            ),
            (
                "", False,
            ),
            (
                None, False,
            ),
        ],
    )
    def test_match(self, cmd_name, expected_result):
        assert Intro().match(cmd_name) == expected_result

    def test_help(self):
        assert Intro().help() == "@wikitransbot intro"
