import warnings

from .base import RequestData, RequestMethod
from .models import *

def _warn_latest_endpoints_deprecated(class_name):
    warnings.warn(
        f"{class_name} is deprecated. The `*/messages/*` wildcard endpoints are not part of the published API spec and may be removed in a future release.",
        DeprecationWarning,
        stacklevel=2,
    )


def _build_query_string(params):
    return '&'.join(f"{key}={value}" for key, value in params.items() if value is not None)


class GetInboxRequest(RequestData):
    def __init__(self, domain, inbox, skip=0, limit=50, sort='descending', \
            decode_subject=False, cursor=None, full=None, delete=None, wait=None):
        self.check_parameter(domain, 'domain')
        self.check_parameter(inbox, 'inbox')

        base_url = f'{self._base_url}/domains/{domain}/inboxes/{inbox}'

         # Build query params dynamically
        params = {
            "skip": skip,
            "limit": limit,
            "sort": sort,
            "decode_subject": decode_subject,
            "cursor": cursor,
            "full": full,
            "delete": delete,
            "wait": wait
        }

        # Filter out None values
        query_string = '&'.join(f"{key}={value}" for key, value in params.items() if value is not None)

        # Construct final URL
        url = f"{base_url}?{query_string}" if query_string else base_url

        super().__init__(RequestMethod.GET, url, model=Inbox)

class ListDomainMessagesRequest(RequestData):
    def __init__(self, domain, inbox='*', skip=0, limit=50, sort='descending',
            decode_subject=False, cursor=None, full=None, wait=None, delete=None):
        self.check_parameter(domain, 'domain')

        base_url = f'{self._base_url}/domains/{domain}/inboxes'

        params = {
            "inbox": inbox,
            "skip": skip,
            "limit": limit,
            "sort": sort,
            "decode_subject": decode_subject,
            "cursor": cursor,
            "full": full,
            "wait": wait,
            "delete": delete
        }

        query_string = _build_query_string(params)
        url = f"{base_url}?{query_string}" if query_string else base_url

        super().__init__(RequestMethod.GET, url, model=Inbox)

class GetInboxMessageRequest(RequestData):
    def __init__(self, domain, inbox, message_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(inbox, 'inbox')
        self.check_parameter(message_id, 'message_id')

        url=f'{self._base_url}/domains/{domain}/inboxes/{inbox}/messages/{message_id}'
        super().__init__(RequestMethod.GET, url, model=Message)

class GetMessageRequest(RequestData):
    def __init__(self, domain, message_id, delete=None):
        self.check_parameter(domain, 'domain')
        self.check_parameter(message_id, 'message_id')

        base_url = f'{self._base_url}/domains/{domain}/messages/{message_id}'

        params = {
            "delete": delete
        }

        query_string = '&'.join(f"{key}={value}" for key, value in params.items() if value is not None)

        url = f"{base_url}?{query_string}" if query_string else base_url

        super().__init__(RequestMethod.GET, url, model=Message)

class GetMessageSummaryRequest(RequestData):
    def __init__(self, domain, message_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(message_id, 'message_id')

        url=f'{self._base_url}/domains/{domain}/messages/{message_id}/summary'
        super().__init__(RequestMethod.GET, url, model=MessageSummary)

class GetMessageTextRequest(RequestData):
    def __init__(self, domain, message_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(message_id, 'message_id')

        url=f'{self._base_url}/domains/{domain}/messages/{message_id}/text'
        super().__init__(RequestMethod.GET, url, model=MessageText)

class GetMessageTextPlainRequest(RequestData):
    def __init__(self, domain, message_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(message_id, 'message_id')

        url=f'{self._base_url}/domains/{domain}/messages/{message_id}/textplain'
        super().__init__(RequestMethod.GET, url, model=MessageTextPlain)

class GetMessageTextHtmlRequest(RequestData):
    def __init__(self, domain, message_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(message_id, 'message_id')

        url=f'{self._base_url}/domains/{domain}/messages/{message_id}/texthtml'
        super().__init__(RequestMethod.GET, url, model=MessageTextHtml)

class GetMessageHeadersRequest(RequestData):
    def __init__(self, domain, message_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(message_id, 'message_id')

        url=f'{self._base_url}/domains/{domain}/messages/{message_id}/headers'
        super().__init__(RequestMethod.GET, url, model=MessageHeaders)

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

class GetMessageLinksFullRequest(RequestData):
    def __init__(self, domain, message_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(message_id, 'message_id')

        url=f'{self._base_url}/domains/{domain}/messages/{message_id}/linksfull'
        super().__init__(RequestMethod.GET, url, model=LinksFull)

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
        _warn_latest_endpoints_deprecated(self.__class__.__name__)
        self.check_parameter(domain, 'domain')

        url=f'{self._base_url}/domains/{domain}/messages/*'
        super().__init__(RequestMethod.GET, url, model=LatestMessages)

class GetLatestInboxMessagesRequest(RequestData):
    def __init__(self, domain, inbox):
        _warn_latest_endpoints_deprecated(self.__class__.__name__)
        self.check_parameter(domain, 'domain')
        self.check_parameter(inbox, 'inbox')

        url=f'{self._base_url}/domains/{domain}/inboxes/{inbox}/messages/*'
        super().__init__(RequestMethod.GET, url, model=LatestMessages)
      
