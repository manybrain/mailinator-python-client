import warnings

from .base import RequestData, RequestMethod
from .models import *


def _warn_domain_management_deprecated(class_name):
    warnings.warn(
        f"{class_name} is deprecated. Create/Delete Domain endpoints are deprecated and may be removed in a future release.",
        DeprecationWarning,
        stacklevel=2,
    )

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
    """Deprecated: Create Domain endpoint is deprecated."""

    def __init__(self, domain_id):
        _warn_domain_management_deprecated(self.__class__.__name__)
        self.check_parameter(domain_id, 'domain_id')

        url=f'{self._base_url}/domains/{domain_id}'
        super().__init__(RequestMethod.POST, url)

class DeleteDomainRequest(RequestData):
    """Deprecated: Delete Domain endpoint is deprecated."""

    def __init__(self, domain_id):
        _warn_domain_management_deprecated(self.__class__.__name__)
        self.check_parameter(domain_id, 'domain_id')

        url=f'{self._base_url}/domains/{domain_id}'
        super().__init__(RequestMethod.DELETE, url)
