import enum


class BaseModel:
    def __str__(self):
        return str(self.__dict__.copy())   


## Condition
##

class Condition(BaseModel):

    class OperationType(enum.Enum):
        EQUALS = "EQUALS"
        PREFIX = "PREFIX"

    def __init__(self, operation=OperationType.EQUALS, field=None, \
                    value=None, *args, **kwargs):
        self.operation = operation or self.OperationType.EQUALS
        self.field = field
        self.value = value
        if 'condition_data' in kwargs:
            self.field = kwargs['condition_data']['field']
            self.value = kwargs['condition_data']['value']

     

    def to_json(self):
        ret_val = self.__dict__.copy()

        ret_val['operation'] = self.operation.value
        ret_val.pop('field')
        ret_val.pop('value')
        ret_val['condition_data'] = {
            'field': self.field, 'value': self.value
        }

        return ret_val

## ACTION
##

class Action(BaseModel):

    class ActionType(enum.Enum):
        WEBHOOK = "WEBHOOK"
        DROP = "DROP"

    class ActionData:
        url = None
        def __init__(self, url=None, *args, **kwargs):
            self.url = url

        def to_json(self):
            return self.__dict__.copy()

    def __init__(self, action=ActionType.DROP, \
                action_data=None, destination=None, \
                *args, **kwargs):
        self.action = action or self.ActionType.DROP
        self.destination = destination
        if action_data is not None:
            self.action_data = action_data \
                if isinstance(action_data, self.ActionData) else self.ActionData(action_data)
        self.destination = destination

    def to_json(self):
        ret_val = self.__dict__.copy()
        ret_val['action'] = self.action.value
        ret_val['action_data'] = self.action_data.to_json()
        if ret_val['destination'] is None:
            ret_val.pop('destination')
        return ret_val

## Rule
##

class Rule(BaseModel):
    class MatchType(enum.Enum):
        ANY = "ANY"
        ALL = "ALL"
        ALWAYS_MATCH = "ALWAYS_MATCH"

        def __str__(self):
            return str(self.value)


    
    def __init__(self, _id=None, description=None, enabled=False,
            match_type=MatchType.ANY, name=None, priority=0, \
            conditions=[], actions=[], \
            *args, **kwargs):
        self._id = _id
        self.description = description or ''
        self.enabled = enabled or False

        # Create Match Type
        self.match_type = match_type or self.MatchType.ANY


        self.name = name or ''
        self.priority = priority or 0
        # Conditions
        if conditions is not None:
            self.conditions = conditions if len(conditions)>0 and isinstance(conditions[0], Condition) \
                        else [Condition(**k) for k in conditions ]
        # Actions
        if actions is not None:
            self.actions = actions if len(actions)>0 and isinstance(actions[0], Action) \
                                else [Action(**k) for k in actions ]


    def to_json(self):       
        ret_val = self.__dict__.copy()
        if self._id is None and '_id' in ret_val:
            ret_val.pop( '_id' )
        ret_val['match_type'] = self.match_type.value
        ret_val['conditions'] = [condition.to_json() for condition in self.conditions]
        ret_val['actions'] = [action.to_json() for action in self.actions]
        return ret_val

# NOTE: This is dumb for me
class Rules(BaseModel):

    def __init__(self, rules=None, *args, **kwargs):
        # Create Rules object
        if rules is not None:        
            self.rules = rules if isinstance(rules, Rules) \
                                else [Rule(**k) for k in rules ]
        else:
            self.rules = []


## Domain
##

class Domain:

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
        return str(self.__dict__.copy())

# NOTE: This is dumb for me
class Domains:

    def __init__(self, domains=[], *args, **kwargs):
        # Create Domains object
        domains = domains or []
        self.domains = domains if isinstance(domains, Domains) \
                    else [Domain(**k) for k in domains ]
    
    def __str__(self):
        return str(self.__dict__.copy())

## Inbox
##
    
class Inbox(BaseModel):

    def __init__(self, domain='', to='', msgs=[], *args, **kwargs):
        self.domain = domain or ''
        self.to = to or ''
        msgs = msgs or []
        self.msgs = msgs if len(msgs)>0 and isinstance(msgs[0], Message) \
                    else [Message(**k) for k in msgs ]
    
class Message(BaseModel):


    def __init__(self, fromfull='', headers={}, subject='', \
                    parts=[], _from='', to='', id='', time=0, seconds_ago=0, \
                    domain='', origfrom='', mrid='', size=0, \
                    stream='', msgType='', source='', text='', \
                    *args, **kwargs):
        self.fromfull = fromfull or ''
        self.headers = headers.copy() if headers is not None else {}
        self.subject = subject or ''
        self.parts = parts if len(parts)>0 and isinstance(parts[0], Part) \
                    else [Part(**k) for k in parts ]
        if 'from' in kwargs:
            self._from = kwargs['from']
        else:
            self._from = _from or ''
        self.to = to or ''
        self.id = id or ''
        self.time = time or 0
        self.seconds_ago = seconds_ago or 0
        self.domain = domain or ''
        self.origfrom = origfrom or ''
        self.mrid = mrid or ''
        self.size = size or 0
        self.stream = stream or ''
        self.msgType = msgType or ''
        self.source = source or ''
        self.text = text or ''

class Part(BaseModel):

    def __init__(self, headers={}, body='', \
                *args, **kwargs):
        self.headers = headers.copy() if headers is not None else {}
        self.body = body or ''


class Attachment(BaseModel):

    def __init__(self, filename='', content_disposition='', \
                content_transfer_encoding='', content_type='', attachment_id='', \
                *args, **kwargs):
        self.filename = filename or ''

        if 'content-disposition' in kwargs:
            self.content_disposition = kwargs['content-disposition']
        else:
            self.content_disposition = content_disposition or ''
        
        if 'content-disposition' in kwargs:
            self.content_transfer_encoding = kwargs['content-disposition']
        else:
            self.content_transfer_encoding = content_transfer_encoding or ''

        if 'content-type' in kwargs:
            self.content_type = kwargs['content-type']
        else:
            self.content_type = content_type or ''
        
        if 'attachment-id' in kwargs:
            self.attachment_id = kwargs['attachment-id']
        else:
            self.attachment_id = attachment_id or ''                                    

class Attachments(BaseModel):
    attachments = None
    
    def __init__(self, attachments=[], *args, **kwargs):
        # Create Domains object
        attachments = attachments or []
        self.attachments = attachments if len(attachments)>0 and isinstance(attachments[0], Attachment) \
                    else [Attachment(**k) for k in attachments ]