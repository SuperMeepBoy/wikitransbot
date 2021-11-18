import tempfile

from wikitransbot import main as wt_bot


def test_get_since_id():
    with tempfile.NamedTemporaryFile() as tmp_file:
        tmp_file.write(b'1000')
        tmp_file.flush()
        assert(wt_bot.get_since_id(tmp_file.name) == 1000)
