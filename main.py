import requests
import json


# Import localsettings if any
try:
    from localsettings import *
except ImportError:
    pass

# Fetch Inbox 
######################
# https://manybrain.github.io/m8rdocs/#fetch-inbox-aka-fetch-message-summaries

#test1@storrellasteam.m8r.co
INBOX = 'test1'
DOMAIN = 'storrellasteam.m8r.co'

headers = {'Authorization': API_TOKEN}
response = requests.get(f'https://mailinator.com/api/v2/domains/{DOMAIN}/inboxes/{INBOX}?limit=2&sort=descending', headers=headers)
json_data = json.loads(response.text)

# JSON Data
print(json.dumps(json_data, indent=4))

# Fetch Message
######################
# https://manybrain.github.io/m8rdocs/#fetch-message

message = json_data['msgs'][0]
message_id = message['id']

response = requests.get(f'https://mailinator.com/api/v2/domains/{DOMAIN}/inboxes/{INBOX}/messages/{message_id}', headers=headers)
print("fetch_message ", response.text, message_id)
json_data = json.loads(response.text)

# JSON Data
print(json.dumps(json_data, indent=4))


# Fetch SMS Message
######################
# https://manybrain.github.io/m8rdocs/#fetch-an-sms-messages


