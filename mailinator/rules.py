import warnings

from .base import RequestData, RequestMethod
from .models import *


def _warn_rules_deprecated(class_name):
    warnings.warn(
        f"{class_name} is deprecated. Rules endpoints are deprecated and may be removed in a future release.",
        DeprecationWarning,
        stacklevel=2,
    )


class CreateRuleRequest(RequestData):
    """Deprecated: rules endpoints are deprecated."""

    def __init__(self, domain, data):
        _warn_rules_deprecated(self.__class__.__name__)
        self.check_parameter(domain, 'domain')

        url=f'{self._base_url}/domains/{domain}/rules/'
        super().__init__(RequestMethod.POST, url, model=Rule, json=data.to_json())

class EnableRuleRequest(RequestData):
    """Deprecated: rules endpoints are deprecated."""

    def __init__(self, domain, rule_id):
        _warn_rules_deprecated(self.__class__.__name__)
        self.check_parameter(domain, 'domain')
        self.check_parameter(rule_id, 'rule_id')

        url=f'{self._base_url}/domains/{domain}/rules/{rule_id}?action=enable'
        super().__init__(RequestMethod.PUT, url)

class DisableRuleRequest(RequestData):
    """Deprecated: rules endpoints are deprecated."""

    def __init__(self, domain, rule_id):
        _warn_rules_deprecated(self.__class__.__name__)
        self.check_parameter(domain, 'domain')
        self.check_parameter(rule_id, 'rule_id')

        url=f'{self._base_url}/domains/{domain}/rules/{rule_id}?action=disable'
        super().__init__(RequestMethod.PUT, url)

class GetRulesRequest(RequestData):
    """Deprecated: rules endpoints are deprecated."""

    def __init__(self, domain):
        _warn_rules_deprecated(self.__class__.__name__)
        self.check_parameter(domain, 'domain')

        url=f'{self._base_url}/domains/{domain}/rules/'
        super().__init__(RequestMethod.GET, url, model=Rules)

class GetRuleRequest(RequestData):
    """Deprecated: rules endpoints are deprecated."""

    def __init__(self, domain, rule_id):
        _warn_rules_deprecated(self.__class__.__name__)
        self.check_parameter(domain, 'domain')
        self.check_parameter(rule_id, 'rule_id')

        url=f'{self._base_url}/domains/{domain}/rules/{rule_id}/'

        #print("URL   ", url)
        super().__init__(RequestMethod.GET, url, model=Rules)

class DeleteRuleRequest(RequestData):
    """Deprecated: rules endpoints are deprecated."""

    def __init__(self, domain, rule_id):
        _warn_rules_deprecated(self.__class__.__name__)
        self.check_parameter(domain, 'domain')
        self.check_parameter(rule_id, 'rule_id')

        url=f'{self._base_url}/domains/{domain}/rules/{rule_id}'
        super().__init__(RequestMethod.DELETE, url)
