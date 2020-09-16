from .base import RequestData, RequestMethod

class GetDomainsRequest(RequestData):
    def __init__(self):
        url=f'{self._base_url}/domains'
        super().__init__(RequestMethod.GET, url)

class GetDomainRequest(RequestData):
    def __init__(self, domain):
        self.check_parameter(domain, 'domain')


        url=f'{self._base_url}/domains/{domain}/'
        super().__init__(RequestMethod.GET, url)
