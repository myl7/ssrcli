class SsrcliException(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class RequireMoreArgument(SsrcliException):
    pass


class InvalidArgument(SsrcliException):
    pass


class InvalidSsrUrl(SsrcliException):
    pass


class RequireGit(SsrcliException):
    pass
