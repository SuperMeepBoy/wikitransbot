import re
import urllib.parse
import requests


class CmdNotFound(Exception):
    pass


class InvalidCmd(Exception):
    pass


class SearchNotFound(Exception):
    pass


class SearchFailed(Exception):
    pass


class Cmd:

    def __init__(self, ignored_words):
        self.cmd_regexp = re.compile(f"{CmdBase.prefix} (\\w*)(?: (.*))?$", re.I | re.M)
        self.ignored_words = re.compile("|".join(ignored_words), re.I)

    def exec(self, tweet_text):
        matched = self.cmd_regexp.search(tweet_text)
        if not matched:
            raise CmdNotFound

        cmd_name, search = matched.groups()
        if search:
            search = re.sub("\\s+", " ", self.ignored_words.sub("", search))

        for cls in CmdBase.__subclasses__():
            cmd = cls()
            if not cmd.match(cmd_name):
                continue
            return cmd.do(search)

        raise CmdNotFound


class CmdBase:
    prefix = "@wikitransbot"

    def match(self, cmd_name):
        raise NotImplementedError

    def do(self, search):
        raise NotImplementedError

    def help(self):
        raise NotImplementedError


class Article(CmdBase):
    cmd_name = "article"

    def match(self, cmd_name):
        return cmd_name == self.cmd_name

    def do(self, search):
        if not search:
            raise InvalidCmd
        base_url = "https://wikitrans.co/wp-admin/admin-ajax.php"
        parameters = "?action=jet_ajax_search&search_taxonomy%5D=&data%5Bvalue%5D="
        url = base_url + parameters

        response = requests.get(f"{url}{urllib.parse.quote(search)}")
        if response.status_code != 200:
            raise SearchFailed

        data = response.json()["data"]
        if not data["post_count"]:
            raise SearchNotFound

        return data["posts"][0]["link"]

    def help(self):
        return f"{self.prefix} {self.cmd_name} recherche"


class Intro(CmdBase):
    default_name = "intro"

    def match(self, cmd_name):
        return cmd_name in [
            self.default_name,
            "transidentité",
            "transidentite",
        ]

    def do(self, _):
        return "https://wikitrans.co/intro/"

    def help(self):
        return f"{self.prefix} {self.default_name}"
