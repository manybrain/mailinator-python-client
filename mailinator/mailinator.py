import requests
from http import HTTPStatus

class Mailinator:

    token = None
    domain = None

    __headers = {}
    __base_url = 'https://mailinator.com/api/v2'

    def __init__(self, token, domain):
        self.domain = domain
        self.token = token
        if self.token is None:
            raise ValueError('Token cannot be None')

        self.headers = {'Authorization': self.token}

    #########################
    ## MESSAGE API
    #########################

    def fetch_inbox(self, inbox):
        if inbox is None:
            raise ValueError('Token cannot be None')
        url=f'{self.__base_url}/domains/{self.domain}/inboxes/{inbox}?limit=2&sort=descending'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def fetch_message(self, inbox, message_id):
        if inbox is None:
            raise ValueError('inbox cannot be None')
        if message_id is None:
            raise ValueError('inbox cannot be None')

        url=f'{self.__base_url}/domains/{self.domain}/inboxes/{inbox}/messages/{message_id}'
        response = requests.get(url, headers=self.headers)
        return response.json()


    def fetch_sms_inbox(self, sms_inbox, sms_team_number):
        if sms_inbox is None:
            raise ValueError('sms_inbox cannot be None')
        if sms_team_number is None:
            raise ValueError('sms_team_member cannot be None')

        url=f'{self.__base_url}/domains/{sms_inbox}/inboxes/{sms_team_number}'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def fetch_message_list_attachments(self, inbox, message_id):
        if inbox is None:
            raise ValueError('inbox cannot be None')
        if message_id is None:
            raise ValueError('inbox cannot be None')

        url=f'{self.__base_url}/domains/{self.domain}/inboxes/{inbox}/messages/{message_id}/attachments'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def fetch_message_attachment(self, inbox, message_id, attachment_id, output_filename):
        url=f'https://mailinator.com/api/v2/domains/{self.domain}/inboxes/{inbox}/messages/{message_id}/attachments/{attachment_id}'
        response = requests.get(url, headers=self.headers)
        # print(" ", response.content)
        # json_data = json.loads(response.text)

        with open(output_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    def delete_message(self, inbox, message_id):
        
        if inbox is None:
            raise ValueError('INBOX cannot be None')
        # Delete inbox
        url=f'{self.__base_url}/{self.domain}/inboxes/{inbox}/messages/{message_id}'
        requests.delete(url, headers=self.headers)

    def delete_inbox(self, inbox):
        if inbox is None:
            raise ValueError('INBOX cannot be None')
        # Delete inbox
        url=f'{self.__base_url}/{self.domain}/inboxes/{inbox}'
        requests.delete(url, headers=self.headers)


    def delete_domain(self):
        url=f'{self.__base_url}/{self.domain}/inboxes'
        requests.delete(url, headers=self.headers)

    #########################
    ## DOMAIN API
    #########################

    def get_all_domains(self):
        url=f'{self.__base_url}/domains/'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_domain(self, id):
        url=f'{self.__base_url}/domains/{id}'
        response = requests.get(url, headers=self.headers)
        return response.json()

    #########################
    ## RULES API
    #########################

    def create_rule(self, data):
        url=f'{self.__base_url}/domains/{self.domain}/rules/'
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()


    def enable_rule(self, id):
        url=f'{self.__base_url}/domains/{self.domain}/rules/{id}?action=enable'
        response = requests.put(url, headers=self.headers)
        return response.status_code == HTTPStatus.OK

    def disable_rule(self, id):
        url=f'{self.__base_url}/domains/{self.domain}/rules/{id}?action=enable'
        response = requests.put(url, headers=self.headers)
        return response.status_code == HTTPStatus.OK

    def get_all_rules(self):
        url=f'{self.__base_url}/domains/{self.domain}/rules/'
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def get_rule(self, id):
        url=f'{self.__base_url}/domains/{self.domain}/rules/{id}'
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def delete_rule(self, id):
        url=f'{self.__base_url}/domains/{self.domain}/rules/{id}'
        response = requests.delete(url, headers=self.headers)
        return response.json()