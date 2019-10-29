class SsrcliException(Exception):
    pass


class SsrUrlInvalid(SsrcliException):
    pass


class RequireMoreParam(SsrcliException):
    def __init__(self, param: str = ''):
        super().__init__()
        self.param = param


class InvalidParam(SsrcliException):
    def __init__(self, param: str = ''):
        super().__init__()
        self.param = param


class NoSuchOperation(SsrcliException):
    def __init__(self, action: str = ''):
        super().__init__()
        self.action = action
