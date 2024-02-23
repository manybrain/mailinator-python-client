from .base import RequestData, RequestMethod
from .models import *

class PublicWebhookRequest(RequestData):
    def __init__(self, data):
        url=f'{self._base_url}/domains/public/webhook/'
        super().__init__(RequestMethod.POST, url, model=Webhook, json=data.to_json())

class PublicInboxWebhookRequest(RequestData):
    def __init__(self, inbox, data):
        self.check_parameter(inbox, 'inbox')
        url=f'{self._base_url}/domains/public/webhook/{inbox}'
        super().__init__(RequestMethod.POST, url, model=Webhook, json=data.to_json())

class PublicCustomServiceWebhookRequest(RequestData):
    def __init__(self, customService, data):
        self.check_parameter(customService, 'customService')
        url=f'{self._base_url}/domains/public/{customService}'
        super().__init__(RequestMethod.POST, url, model=Webhook, json=data.to_json())
        
class PublicCustomServiceInboxWebhookRequest(RequestData):
    def __init__(self, customService, inbox, data):
        self.check_parameter(customService, 'customService')
        self.check_parameter(inbox, 'inbox')
        url=f'{self._base_url}/domains/public/{customService}/{inbox}'
        super().__init__(RequestMethod.POST, url, model=Webhook, json=data.to_json())

class PrivateWebhookRequest(RequestData):
    def __init__(self, whToken, data):
        self.check_parameter(whToken, 'whToken')
        url=f'{self._base_url}/domains/{whToken}/webhook/'
        super().__init__(RequestMethod.POST, url, model=Webhook, json=data.to_json())

class PrivateInboxWebhookRequest(RequestData):
    def __init__(self, whToken, inbox, data):
        self.check_parameter(whToken, 'whToken')
        self.check_parameter(inbox, 'inbox')
        url=f'{self._base_url}/domains/{whToken}/webhook/{inbox}'
        super().__init__(RequestMethod.POST, url, model=Webhook, json=data.to_json())

class PrivateCustomServiceWebhookRequest(RequestData):
    def __init__(self, whToken, customService, data):
        self.check_parameter(whToken, 'whToken')
        self.check_parameter(customService, 'customService')
        url=f'{self._base_url}/domains/{whToken}/{customService}'
        super().__init__(RequestMethod.POST, url, model=Webhook, json=data.to_json())
        
class PrivateCustomServiceInboxWebhookRequest(RequestData):
    def __init__(self, whToken, customService, inbox, data):
        self.check_parameter(whToken, 'whToken')
        self.check_parameter(customService, 'customService')
        self.check_parameter(inbox, 'inbox')
        url=f'{self._base_url}/domains/{whToken}/{customService}/{inbox}'
        super().__init__(RequestMethod.POST, url, model=Webhook, json=data.to_json())
