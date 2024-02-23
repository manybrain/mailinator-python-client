from .base import RequestData, RequestMethod
from .models import *

class GetInboxRequest(RequestData):
    def __init__(self, domain, inbox, skip=0, limit=50, sort='descending', \
            decode_subject=False):
        self.check_parameter(domain, 'domain')
        self.check_parameter(inbox, 'inbox')

        url=f'{self._base_url}/domains/{domain}/inboxes/{inbox}?'
        url = url + (f'skip={skip}' if skip is not None else '')
        url = url + (f'&limit={limit}' if limit is not None else '')
        url = url + (f'&sort={sort}' if sort is not None else '')
        url = url + (f'&decode_subject={decode_subject}' if decode_subject is not None else '')
        super().__init__(RequestMethod.GET, url, model=Inbox)

class GetInboxMessageRequest(RequestData):
    def __init__(self, domain, inbox, message_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(inbox, 'inbox')
        self.check_parameter(message_id, 'message_id')

        url=f'{self._base_url}/domains/{domain}/inboxes/{inbox}/messages/{message_id}'
        super().__init__(RequestMethod.GET, url, model=Message)

class GetMessageRequest(RequestData):
    def __init__(self, domain, message_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(message_id, 'message_id')

        url=f'{self._base_url}/domains/{domain}/messages/{message_id}'
        super().__init__(RequestMethod.GET, url, model=Message)

class GetSmsInboxRequest(RequestData):
    def __init__(self, domain, phone_number):
        self.check_parameter(domain, 'domain')
        self.check_parameter(phone_number, 'phone_number')

        url=f'{self._base_url}/domains/{domain}/inboxes/{phone_number}'
        super().__init__(RequestMethod.GET, url, model=Inbox)

class GetInboxMessageAttachmentsRequest(RequestData):
    def __init__(self, domain, inbox, message_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(inbox, 'inbox')
        self.check_parameter(message_id, 'message_id')
        
        url=f'{self._base_url}/domains/{domain}/inboxes/{inbox}/messages/{message_id}/attachments'
        super().__init__(RequestMethod.GET, url, model=Attachments)


class GetMessageAttachmentsRequest(RequestData):
    def __init__(self, domain, message_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(message_id, 'message_id')
        
        url=f'{self._base_url}/domains/{domain}/messages/{message_id}/attachments'
        super().__init__(RequestMethod.GET, url, model=Attachments)

class GetInboxMessageAttachmentRequest(RequestData):
    def __init__(self, domain, inbox, message_id, attachment_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(inbox, 'inbox')
        self.check_parameter(message_id, 'message_id')
        self.check_parameter(attachment_id, 'attachment_id')

        url=f'{self._base_url}/domains/{domain}/inboxes/{inbox}/messages/{message_id}/attachments/{attachment_id}'
        super().__init__(RequestMethod.GET, url)
   
class GetMessageAttachmentRequest(RequestData):
    def __init__(self, domain, message_id, attachment_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(message_id, 'message_id')
        self.check_parameter(attachment_id, 'attachment_id')

        url=f'{self._base_url}/domains/{domain}/messages/{message_id}/attachments/{attachment_id}'
        super().__init__(RequestMethod.GET, url)

class GetMessageLinksRequest(RequestData):
    def __init__(self, domain, message_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(message_id, 'message_id')

        url=f'{self._base_url}/domains/{domain}/messages/{message_id}/links'
        super().__init__(RequestMethod.GET, url, model=Links)

class GetInboxMessageLinksRequest(RequestData):
    def __init__(self, domain, inbox, message_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(inbox, 'inbox')
        self.check_parameter(message_id, 'message_id')

        url=f'{self._base_url}/domains/{domain}/inboxes/{inbox}/messages/{message_id}/links'
        super().__init__(RequestMethod.GET, url, model=Links)

class DeleteDomainMessagesRequest(RequestData):
    def __init__(self, domain):
        self.check_parameter(domain, 'domain')

        url=f'{self._base_url}/domains/{domain}/inboxes'
        super().__init__(RequestMethod.DELETE, url)

class DeleteInboxMessagesRequest(RequestData):
    def __init__(self, domain, inbox):
        self.check_parameter(domain, 'domain')
        self.check_parameter(inbox, 'inbox')
        
        url=f'{self._base_url}/domains/{domain}/inboxes/{inbox}'
        super().__init__(RequestMethod.DELETE, url)

class DeleteMessageRequest(RequestData):
    def __init__(self, domain, inbox, message_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(inbox, 'inbox')
        self.check_parameter(message_id, 'message_id')

        url=f'{self._base_url}/domains/{domain}/inboxes/{inbox}/messages/{message_id}'
        super().__init__(RequestMethod.DELETE, url)

class PostMessageRequest(RequestData):
    def __init__(self, domain, inbox, data):
        self.check_parameter(domain, 'domain')
        self.check_parameter(inbox, 'inbox')

        url=f'{self._base_url}/domains/{domain}/inboxes/{inbox}'
        super().__init__(RequestMethod.POST, url, model=PostMessage, json=data.to_json())  

class GetMessageSmtpLogRequest(RequestData):
    def __init__(self, domain, message_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(message_id, 'message_id')

        url=f'{self._base_url}/domains/{domain}/messages/{message_id}/smtplog'
        super().__init__(RequestMethod.GET, url, model=SmtpLogs)

class GetInboxMessageSmtpLogRequest(RequestData):
    def __init__(self, domain, inbox, message_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(inbox, 'inbox')
        self.check_parameter(message_id, 'message_id')

        url=f'{self._base_url}/domains/{domain}/inboxes/{inbox}/messages/{message_id}/smtplog'
        super().__init__(RequestMethod.GET, url, model=SmtpLogs)  

class GetMessageRawRequest(RequestData):
    def __init__(self, domain, message_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(message_id, 'message_id')

        url=f'{self._base_url}/domains/{domain}/messages/{message_id}/raw'
        super().__init__(RequestMethod.GET, url, model=RawData)

class GetInboxMessageRawRequest(RequestData):
    def __init__(self, domain, inbox, message_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(inbox, 'inbox')
        self.check_parameter(message_id, 'message_id')

        url=f'{self._base_url}/domains/{domain}/inboxes/{inbox}/messages/{message_id}/raw'
        super().__init__(RequestMethod.GET, url, model=RawData)

class GetLatestMessagesRequest(RequestData):
    def __init__(self, domain):
        self.check_parameter(domain, 'domain')

        url=f'{self._base_url}/domains/{domain}/messages/*'
        super().__init__(RequestMethod.GET, url, model=LatestMessages)

class GetLatestInboxMessagesRequest(RequestData):
    def __init__(self, domain, inbox):
        self.check_parameter(domain, 'domain')
        self.check_parameter(inbox, 'inbox')

        url=f'{self._base_url}/domains/{domain}/inboxes/{inbox}/messages/*'
        super().__init__(RequestMethod.GET, url, model=LatestMessages)
      