from .base import RequestData, RequestMethod
from .models import *

class GetDomainsRequest(RequestData):
    def __init__(self):
        url=f'{self._base_url}/domains'
        super().__init__(RequestMethod.GET, url, Domains)

class GetDomainRequest(RequestData):
    def __init__(self, domain):
        self.check_parameter(domain, 'domain')
        url=f'{self._base_url}/domains/{domain}/'
        super().__init__(RequestMethod.GET, url, Domain)

class CreateDomainRequest(RequestData):
    def __init__(self, domain_id):
        self.check_parameter(domain_id, 'domain_id')

        url=f'{self._base_url}/domains/{domain_id}'
        super().__init__(RequestMethod.POST, url)

class DeleteDomainRequest(RequestData):
    def __init__(self, domain_id):
        self.check_parameter(domain_id, 'domain_id')

        url=f'{self._base_url}/domains/{domain_id}'
        super().__init__(RequestMethod.DELETE, url)