import warnings

from .base import RequestData, RequestMethod
from .models import *


def _warn_singular_authenticator_deprecated(class_name):
    warnings.warn(
        f"{class_name} is deprecated. Use the plural /authenticators/ endpoint request classes instead.",
        DeprecationWarning,
        stacklevel=2,
    )


class InstantTOTP2FACodeRequest(RequestData):
    def __init__(self, totp_secret_key):
        self.check_parameter(totp_secret_key, 'totp_secret_key')
        url=f'{self._base_url}/totp/{totp_secret_key}'
        super().__init__(RequestMethod.GET, url)

class GetAuthenticatorsRequest(RequestData):
    def __init__(self):
        url=f'{self._base_url}/authenticators/'
        super().__init__(RequestMethod.GET, url)

class GetAuthenticatorsByIdRequest(RequestData):
    def __init__(self, id):
        self.check_parameter(id, 'id')
        url=f'{self._base_url}/authenticators/{id}'
        super().__init__(RequestMethod.GET, url)
        
class GetAuthenticatorRequest(RequestData):
    def __init__(self):
        _warn_singular_authenticator_deprecated(self.__class__.__name__)
        url=f'{self._base_url}/authenticators/'
        super().__init__(RequestMethod.GET, url)

class GetAuthenticatorByIdRequest(RequestData):
    def __init__(self, id):
        _warn_singular_authenticator_deprecated(self.__class__.__name__)
        self.check_parameter(id, 'id')
        url=f'{self._base_url}/authenticators/{id}'
        super().__init__(RequestMethod.GET, url)
