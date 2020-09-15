import requests
from http import HTTPStatus
import enum


class RequestMethod(enum.Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"

class RequestData:
    _base_url = 'https://mailinator.com/api/v2'

    method = None
    url = None
    json = None

    def __init__(self, method, url, json=None):
        self.method = method
        self.url = url
        self.json = json

#########################
## MESSAGE API
#########################

class GetInboxRequest(RequestData):
    def __init__(self, domain, inbox):
        if domain is None:
            raise ValueError('domain cannot be None')
        if inbox is None:
            raise ValueError('inbox cannot be None')


        url=f'{self._base_url}/domains/{domain}/inboxes/{inbox}?limit=2&sort=descending'
        super().__init__(RequestMethod.GET, url)

class GetMessageRequest(RequestData):
    def __init__(self, domain, inbox, message_id):
        if domain is None:
            raise ValueError('domain cannot be None')
        if inbox is None:
            raise ValueError('inbox cannot be None')
        if message_id is None:
            raise ValueError('message_id cannot be None')

        url=f'{self._base_url}/domains/{domain}/inboxes/{inbox}/messages/{message_id}'
        super().__init__(RequestMethod.GET, url)

class GetSmsInboxRequest(RequestData):
    def __init__(self, domain, phone_number):
        if domain is None:
            raise ValueError('domain cannot be None')
        if phone_number is None:
            raise ValueError('phone_number cannot be None')


        url=f'{self._base_url}/domains/{domain}/inboxes/{phone_number}'
        super().__init__(RequestMethod.GET, url)

class GetAttachmentsRequest(RequestData):
    def __init__(self, domain, inbox, message_id):
        if domain is None:
            raise ValueError('domain cannot be None')
        if inbox is None:
            raise ValueError('inbox cannot be None')
        if message_id is None:
            raise ValueError('message_id cannot be None')

        url=f'{self._base_url}/domains/{domain}/inboxes/{inbox}/messages/{message_id}/attachments'
        super().__init__(RequestMethod.GET, url)

class GetAttachmentRequest(RequestData):
    def __init__(self, domain, inbox, message_id, attachment_id):
        url=f'{self._base_url}/domains/{domain}/inboxes/{inbox}/messages/{message_id}/attachments/{attachment_id}'
        super().__init__(RequestMethod.GET, url)

class DeleteDomainMessagesRequest(RequestData):
    def __init__(self, domain):
        if domain is None:
            raise ValueError('domain cannot be None')

        url=f'{self._base_url}/domains/{domain}/inboxes'
        super().__init__(RequestMethod.DELETE, url)

class DeleteInboxMessagesRequest(RequestData):
    def __init__(self, domain, inbox):
        if domain is None:
            raise ValueError('domain cannot be None')
        if inbox is None:
            raise ValueError('inbox cannot be None')

        url=f'{self._base_url}/domains/{domain}/inboxes/{inbox}'
        super().__init__(RequestMethod.DELETE, url)

class DeleteMessageRequest(RequestData):
    def __init__(self, domain, inbox, message_id):
        if domain is None:
            raise ValueError('domain cannot be None')
        if inbox is None:
            raise ValueError('inbox cannot be None')
        if message_id is None:
            raise ValueError('message_id cannot be None')

        url=f'{self._base_url}/domains/{domain}/inboxes/{inbox}/messages/{message_id}'
        super().__init__(RequestMethod.DELETE, url)

#########################
## DOMAIN API
#########################

class GetDomainsRequest(RequestData):
    def __init__(self):
        url=f'{self._base_url}/domains'
        super().__init__(RequestMethod.GET, url)

class GetDomainRequest(RequestData):
    def __init__(self, domain):
        if domain is None:
            raise ValueError('domain cannot be None')

        url=f'{self._base_url}/domains/{domain}/'
        super().__init__(RequestMethod.GET, url)

class Mailinator:

    token = None

    __headers = {}
    __base_url = 'https://mailinator.com/api/v2'

    def __init__(self, token):
        self.token = token
        if self.token is None:
            raise ValueError('Token cannot be None')

        self.headers = {'Authorization': self.token}

    def request( self, request_data ):
        if request_data.method == RequestMethod.GET:
            response = requests.get(request_data.url, headers=self.headers)
        elif request_data.method == RequestMethod.POST:
            response = requests.post(request_data.url, json=request_data.json, headers=self.headers)
        elif request_data.method == RequestMethod.PUT:
            response = requests.put(request_data.url, headers=self.headers)
        elif request_data.method == RequestMethod.DELETE:
            response = requests.delete(request_data.url, headers=self.headers)
        else:
            raise Exception(f"Method not identified {request_data.method}")

        # Check that response is OK
        if response.status_code != HTTPStatus.OK:
            raise Exception("Request returned no ok")

        if response.headers['Content-Type'] == 'application/json':
            return response.json()
        else:
            return response


    #########################
    ## RULES API
    #########################

    def create_rule(self, domain, data):
        url=f'{self.__base_url}/domains/{domain}/rules/'
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

    def enable_rule(self, domain, id):
        url=f'{self.__base_url}/domains/{domain}/rules/{id}?action=enable'
        response = requests.put(url, headers=self.headers)
        return response.status_code == HTTPStatus.OK

    def disable_rule(self, domain, id):
        url=f'{self.__base_url}/domains/{domain}/rules/{id}?action=enable'
        response = requests.put(url, headers=self.headers)
        return response.status_code == HTTPStatus.OK

    def get_all_rules(self, domain):
        url=f'{self.__base_url}/domains/{domain}/rules/'
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def get_rule(self, domain, id):
        url=f'{self.__base_url}/domains/{domain}/rules/{id}'
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def delete_rule(self, domain, id):
        url=f'{self.__base_url}/domains/{domain}/rules/{id}'
        response = requests.delete(url, headers=self.headers)
        return response.json()