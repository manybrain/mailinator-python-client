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
    __base_url = 'https://api.mailinator.com/api/v2'
    __version = '0.0.7'  # Change this to your SDK version
    __timeout = 125 # Set timeout to 65 sec

    def __init__(self, token=None):
        self.token = token
        user_agent = f"Mailinator SDK - Python V{self.__version}"
        if token is not None:
            self.headers = {
                'Authorization': self.token,
                'User-Agent': user_agent
            }
        else:
            self.headers = {'User-Agent': user_agent}

    def request( self, request_data ):
        if request_data.method == RequestMethod.GET:
            response = requests.get(request_data.url, headers=self.headers, timeout=self.__timeout)
        elif request_data.method == RequestMethod.POST:
            response = requests.post(request_data.url, json=request_data.json, headers=self.headers, timeout=self.__timeout)
        elif request_data.method == RequestMethod.PUT:
            response = requests.put(request_data.url, headers=self.headers, timeout=self.__timeout)
        elif request_data.method == RequestMethod.DELETE:
            response = requests.delete(request_data.url, headers=self.headers, timeout=self.__timeout)
        else:
            raise MailinatorException(f"Method not identified {request_data.method}")

        # Check that response is OK
        if response.status_code == HTTPStatus.OK or \
             response.status_code == HTTPStatus.NO_CONTENT:
            pass
        else:
            raise MailinatorException(f"Request failed with status code {response.status_code}. Response: {response.content}")

        if 'Content-Type' in response.headers and \
            response.headers['Content-Type'] == 'application/json':
            if request_data.model is not None:
                #print("reponse.json() ", response.json())
                return request_data.model(**response.json())
            else:
                return response.json()
        else:
            return response

