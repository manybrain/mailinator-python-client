from .base import RequestData, RequestMethod
from .models import *

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
        url=f'{self._base_url}/authenticator/'
        super().__init__(RequestMethod.GET, url)

class GetAuthenticatorByIdRequest(RequestData):
    def __init__(self, id):
        self.check_parameter(id, 'id')
        url=f'{self._base_url}/authenticator/{id}'
        super().__init__(RequestMethod.GET, url)