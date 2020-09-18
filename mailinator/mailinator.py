import requests
from http import HTTPStatus


from .base import RequestData, RequestMethod


class MailinatorException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


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
            raise MailinatorException(f"Method not identified {request_data.method}")

        # Check that response is OK
        if response.status_code == HTTPStatus.OK or \
             response.status_code == HTTPStatus.NO_CONTENT:
            pass
        else:
            raise MailinatorException("Request returned no ok")

        

        if 'Content-Type' in response.headers and \
            response.headers['Content-Type'] == 'application/json':
            if request_data.model is not None:
                #print("reponse.json() ", response.json())
                return request_data.model(**response.json())
            else:
                return response.json()

            #return response.json()
        else:
            return response

