from .base import RequestData, RequestMethod

class CreateRuleRequest(RequestData):
    def __init__(self, domain, data):
        self.check_parameter(domain, 'domain')

        url=f'{self._base_url}/domains/{domain}/rules/'
        super().__init__(RequestMethod.POST, url, data)

class EnableRuleRequest(RequestData):
    def __init__(self, domain, rule_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(rule_id, 'rule_id')

        url=f'{self._base_url}/domains/{domain}/rules/{rule_id}?action=enable'
        super().__init__(RequestMethod.PUT, url)

class DisableRuleRequest(RequestData):
    def __init__(self, domain, rule_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(rule_id, 'rule_id')

        url=f'{self._base_url}/domains/{domain}/rules/{rule_id}?action=enable'
        super().__init__(RequestMethod.PUT, url)

class GetRulesRequest(RequestData):
    def __init__(self, domain):
        self.check_parameter(domain, 'domain')

        url=f'{self._base_url}/domains/{domain}/rules/'
        super().__init__(RequestMethod.GET, url)

class GetRuleRequest(RequestData):
    def __init__(self, domain, rule_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(rule_id, 'rule_id')

        url=f'{self._base_url}/domains/{domain}/rules/{rule_id}'
        super().__init__(RequestMethod.GET, url)

class DeleteRuleRequest(RequestData):
    def __init__(self, domain, rule_id):
        self.check_parameter(domain, 'domain')
        self.check_parameter(rule_id, 'rule_id')

        url=f'{self._base_url}/domains/{domain}/rules/{rule_id}'
        super().__init__(RequestMethod.DELETE, url)

