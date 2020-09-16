import enum




## Condition
##

class Condition:

    class OperationType:
        EQUALS = "EQUALS"
        PREFIX = "PREFIX"

    operation = OperationType.EQUALS
    field = None
    value = None

    def __init__(self, operation=OperationType.EQUALS, field=None, \
                    value=None, *args, **kwargs):
        self.operation = operation 
        self.field = field
        self.value = value
        if 'condition_data' in kwargs:
            self.field = kwargs['condition_data']['field']
            self.value = kwargs['condition_data']['value']

    def __str__(self):
        return str(self.__dict__)        

    def to_json(self):
        ret_val = self.__dict__.copy()

        ret_val.pop('field')
        ret_val.pop('value')
        ret_val['condition_data'] = {
            'field': self.field, 'value': self.value
        }

        return ret_val

## ACTION
##

class Action:

    class ActionType:
        WEBHOOK = "WEBHOOK"
        DROP = "DROP"

    class ActionData:
        url = None
        def __init__(self, url=None, *args, **kwargs):
            self.url = url

        def to_json(self):
            return self.__dict__.copy()

    action = None
    action_data = None
    destination = None

    def __init__(self, action=ActionType.DROP, \
                action_data=None, destination=None, \
                *args, **kwargs):
        self.action = action
        self.destination = destination
        if action_data is not None:
            self.action_data = action_data \
                if isinstance(action_data, self.ActionData) else self.ActionData(action_data)
        self.destination = destination

    def __str__(self):
        return str(self.__dict__)        


    def to_json(self):
        ret_val = self.__dict__.copy()
        ret_val['action_data'] = self.action_data.to_json()
        if ret_val['destination'] is None:
            ret_val.pop('destination')
        return ret_val

## ACTION
##

class Rule:
    class MatchType:
        ANY = "ANY"
        ALL = "ALL"
        ALWAYS_MATCH = "ALWAYS_MATCH"

        def __str__(self):
            return str(self.value)

    _id = None
    description = None
    enabled = None
    match_type = None
    name = None
    priority = 0
    conditions = []
    actions = []
    
    def __init__(self, _id=None, description=None, enabled=False,
            match_type=MatchType.ANY, name=None, priority=0, \
            conditions=None, actions=None, \
            *args, **kwargs):
        self._id = _id
        self.description = description
        self.enabled = enabled

        # Create Match Type     
        self.match_type = match_type


        self.name = name
        self.priority = priority
        # Conditions
        if conditions is not None:
            self.conditions = conditions if isinstance(conditions[0], Condition) \
                        else [Condition(**k) for k in conditions ]
        else:
            self.conditions = []
        # Actions
        if actions is not None:
            self.actions = actions if isinstance(actions[0], Action) \
                                else [Action(**k) for k in actions ]
        else:
            self.actions = []


    def to_json(self):       
        ret_val = self.__dict__.copy()
        if self._id is None and '_id' in ret_val:
            ret_val.pop( '_id' )
        ret_val['conditions'] = [condition.to_json() for condition in self.conditions]
        ret_val['actions'] = [action.to_json() for action in self.actions]
        return ret_val

# NOTE: This is dumb for me
class Rules:
    rules = []

    def __init__(self, rules=None, *args, **kwargs):
        # Create Rules object
        if rules is not None:        
            self.rules = rules if isinstance(rules, Rules) \
                                else [Rule(**k) for k in rules ]
        else:
            self.rules = []

    def __str__(self):
        return str(self.__dict__)

class Domain:
    _id = None
    description = None
    enabled = None
    name = None
    ownerid = None
    rules = []

    def __init__(self, _id=None, description=None, \
            enabled=None, name=None, ownerid=None, rules=None, \
            *args, **kwargs):
        self._id = _id
        self.description = description
        self.enabled = enabled
        self.name = name
        self.ownerid = ownerid
        
        # Create Rules object
        self.rules = rules if isinstance(rules, Rules) else Rules(rules)

    def __str__(self):
        return str(self.__dict__)

# NOTE: This is dumb for me
class Domains:
    domains = []

    def __init__(self, domains=None, *args, **kwargs):
        # Create Domains object
        self.domains = domains if isinstance(domains, Domains) \
                    else [Domain(**k) for k in domains ]
    
    def __str__(self):
        return str(self.__dict__)

    