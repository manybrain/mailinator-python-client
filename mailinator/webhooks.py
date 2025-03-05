from .base import RequestData, RequestMethod
from .models import *

class PrivateWebhookRequest(RequestData):
    def __init__(self, whToken, data):
        self.check_parameter(whToken, 'whToken')
        url=f'{self._base_url}/domains/private/webhook?whtoken={whToken}'
        super().__init__(RequestMethod.POST, url, model=Webhook, json=data.to_json())

class PrivateInboxWebhookRequest(RequestData):
    def __init__(self, whToken, inbox, data):
        self.check_parameter(whToken, 'whToken')
        self.check_parameter(inbox, 'inbox')
        url=f'{self._base_url}/domains/private/webhook/{inbox}?whtoken={whToken}'
        super().__init__(RequestMethod.POST, url, model=Webhook, json=data.to_json())

class PrivateCustomServiceWebhookRequest(RequestData):
    def __init__(self, whToken, customService, data):
        self.check_parameter(whToken, 'whToken')
        self.check_parameter(customService, 'customService')
        url=f'{self._base_url}/domains/private/{customService}?whtoken={whToken}'
        super().__init__(RequestMethod.POST, url, model=Webhook, json=data.to_json())
        
class PrivateCustomServiceInboxWebhookRequest(RequestData):
    def __init__(self, whToken, customService, inbox, data):
        self.check_parameter(whToken, 'whToken')
        self.check_parameter(customService, 'customService')
        self.check_parameter(inbox, 'inbox')
        url=f'{self._base_url}/domains/private/{customService}/{inbox}?whtoken={whToken}'
        super().__init__(RequestMethod.POST, url, model=Webhook, json=data.to_json())
