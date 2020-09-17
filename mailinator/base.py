import enum


class RequestMethod(enum.Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"

class RequestData:
    _base_url = 'https://mailinator.com/api/v2'

    def check_parameter(self, parameter, name):
        if parameter is None:
            raise ValueError(f'{name} cannot be None')

    def __init__(self, method, url, model=None, json=None):
        self.method = method
        self.url = url
        self.model = model
        self.json = json
