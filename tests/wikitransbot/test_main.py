import tempfile

import pytest

from wikitransbot import main as wt_bot


def test_get_since_id():
    with tempfile.NamedTemporaryFile() as tmp_file:
        tmp_file.write(b'1000')
        tmp_file.flush()
        assert(wt_bot.get_since_id(tmp_file.name) == 1000)


@pytest.mark.parametrize("tweet_text, keyword, expected_result", [
    (
        "@wikitransbot article féminiser sa voix",
        "article",
        (
            "https://wikitrans.co/wp-admin/admin-ajax.php?"
            "action=jet_ajax_search&search_taxonomy%5D=&data%5Bvalue%5D=féminiser sa voix"
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
])
def test_build_search_article_url(tweet_text, keyword, expected_result):
    result = wt_bot.build_search_article_url(tweet_text=tweet_text, keyword=keyword)
    assert(result == expected_result)
