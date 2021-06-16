class KedroDiffError(TypeError):
    """
    Error messages related to the kedro diff command.
    """


class RevParseError(BaseException):
    def __init__(self, msg):
        self.msg = msg.decode("utf-8")

    def __str__(self):
        return self.msg.replace("\n", " ")
