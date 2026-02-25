# Examples

Usage examples for the Mailinator Python client.

## Setup

```python
from mailinator import Mailinator

client = Mailinator(API_TOKEN)
```

## Inbox

### Get inbox messages

```python
from mailinator import GetInboxRequest

inbox = client.request(GetInboxRequest(DOMAIN, INBOX))
```

### Get paginated inbox messages

```python
from mailinator import GetInboxRequest

inbox = client.request(
    GetInboxRequest(
        DOMAIN,
        INBOX,
        skip=0,
        limit=50,
        sort="descending",
        decode_subject=False,
    )
)
```

## Messages

### Get a message by ID

```python
from mailinator import GetMessageRequest

message = client.request(GetMessageRequest(DOMAIN, MESSAGE_ID))
```

## More Examples

See integration-style examples in `tests/test_mailinator.py`.
