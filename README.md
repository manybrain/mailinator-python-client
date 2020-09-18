#### [Mailinator](https://www.mailinator.com/) REST API client for Python applications. 

Uses requests(https://requests.readthedocs.io/en/master/) to perform REST request operations

#### Installation

```
pip install mailinator-python-client-2
```

#### Usage example

##### Create MailinatorClient

```python
mailinator = Mailinator(API_TOKEN)
```

###### Get inbox from domain

```python
inbox = mailinator.request( GetInboxRequest(DOMAIN, INBOX) )
```

###### Get paginated messages from domain and inbox

```python
inbox = mailinator.request( GetInboxRequest(DOMAIN, INBOXskip=0, limit=50, \
                        sort='descending', decode_subject=False) )       
```
                                                       
###### Get message
             
```python                                
message = self.mailinator.request( GetMessageRequest(DOMAIN, INBOX, message_id) )
```

#### Build tests

* `pytest -s`

By default, most of the tests are skipped. 

##### Build with tests

Most of the tests require env variables with valid values. Visit tests source code and review `EnabledIfEnvironmentVariable` wrapped parts. The more env variables you set, the more tests are run.

* `MAILINATOR_TEST_API_TOKEN` - API tokens for authentication; basic requirement across many tests;see also https://manybrain.github.io/m8rdocs/#api-authentication
* `MAILINATOR_TEST_DOMAIN_PRIVATE` - private domain; visit https://www.mailinator.com/
* `MAILINATOR_TEST_INBOX` - some already existing inbox within the private domain
* `MAILINATOR_TEST_PHONE_NUMBER` - associated phone number within the private domain; see also https://manybrain.github.io/m8rdocs/#fetch-an-sms-messages
* `MAILINATOR_TEST_MESSAGE_WITH_ATTACHMENT_ID` - existing message id within inbox (see above) within private domain (see above); see also https://manybrain.github.io/m8rdocs/#fetch-message
* `MAILINATOR_TEST_ATTACHMENT_ID` - existing message id within inbox (see above) within private domain (see above); see also https://manybrain.github.io/m8rdocs/#fetch-message
* `MAILINATOR_TEST_DELETE_DOMAIN` - don't use it unless you are 100% sure what you are doing
