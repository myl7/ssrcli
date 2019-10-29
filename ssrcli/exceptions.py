class SsrcliException(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class InvalidSsrUrl(SsrcliException):
    pass


class RequireMoreArgument(SsrcliException):
    pass


class InvalidArgument(SsrcliException):
    pass


class NoSuchOperation(SsrcliException):
    pass
