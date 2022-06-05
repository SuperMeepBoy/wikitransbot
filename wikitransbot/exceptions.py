class InvalidCommandException(ValueError):
    def __init__(self):
        super(InvalidCommandException, self).__init__("Invalid command")
