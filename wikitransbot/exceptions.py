class InvalidCommandException(ValueError):
    def __init__(self):
        super(InvalidCommandException, self).__init__("Invalid command")


class ArticleCommandEmptyRequestException(ValueError):
    def __init__(self):
        super(ArticleCommandEmptyRequestException, self).__init__("Empty request with an article command")
