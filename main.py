import requests
import json
import sys


# Import localsettings if any
try:
    from localsettings import *
except ImportError:
    pass

#test1@storrellasteam.m8r.co
INBOX = 'test1'
DOMAIN = 'storrellasteam.m8r.co'

headers = {'Authorization': API_TOKEN}


# Fetch Inbox 
######################
# https://manybrain.github.io/m8rdocs/#fetch-inbox-aka-fetch-message-summaries

response = requests.get(f'https://mailinator.com/api/v2/domains/{DOMAIN}/inboxes/{INBOX}?limit=2&sort=descending', headers=headers)
json_data = response.json()

# JSON Data
#print(json.dumps(json_data, indent=4))



# from smtplib import SMTP
# import datetime

# debuglevel = 0


# mailserver = SMTP()
# mailserver.set_debuglevel(debuglevel)
# mailserver.connect('in-v3.mailjet.com', 587)

# # identify ourselves to smtp gmail client
# mailserver.ehlo()
# # secure our email with tls encryption
# mailserver.starttls()
# # re-identify ourselves as an encrypted connection
# mailserver.ehlo()


# mailserver.login('3ac62d5d6feba7239d5f0a6ef79f9d0d', 'ff4ab0c9275e3fc3319e7b210a688d38')


# from_addr = "Sergi Torrellas <storrellas@gmail.com>"
# to_addr = "test1@storrellasteam.m8r.co"

# subj = "hello"
# date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )

# message_text = "Hello\nThis is a mail from your server\n\nBye\n"

# msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % ( from_addr, to_addr, subj, date, message_text )

# mailserver.sendmail(from_addr, to_addr, msg)
# mailserver.quit()


import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate



def send_mail(send_from, send_to, subject, text, files=None):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)



    smtp = smtplib.SMTP()
    smtp.connect(SMTP_SERVER, SMTP_PORT)

    # identify ourselves to smtp gmail client
    smtp.ehlo()
    # secure our email with tls encryption
    smtp.starttls()
    # re-identify ourselves as an encrypted connection
    smtp.ehlo()
    smtp.login(SMTP_USERNAME, SMTP_PASSWORD)



    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


send_mail(SMTP_SENDER, ['test1@storrellasteam.m8r.co'], 'MySubject', 'Here my text', files=['./tintin.jpg'])


print("Aborting testing")
sys.exit(0)

# Fetch Message
######################
# https://manybrain.github.io/m8rdocs/#fetch-message

message = json_data['msgs'][0]
message_id = message['id']

response = requests.get(f'https://mailinator.com/api/v2/domains/{DOMAIN}/inboxes/{INBOX}/messages/{message_id}', headers=headers)
json_data = response.json()

# JSON Data
print(json.dumps(json_data, indent=4))


# # Fetch SMS Message
# ######################
# # https://manybrain.github.io/m8rdocs/#fetch-an-sms-messages


# SMS_INBOX = 'public'
# SMS_TEAM_NUMBER = '12013814330'

# response = requests.get(f'https://mailinator.com/api/v2/domains/{SMS_INBOX}/inboxes/{SMS_TEAM_NUMBER}', headers=headers)
# json_data = response.json()

# # JSON Data
# print(json.dumps(json_data, indent=4))





# # Fetch List of Attachments
# ######################
# # https://manybrain.github.io/m8rdocs/#fetch-list-of-attachments


# response = requests.get(f'https://mailinator.com/api/v2/domains/{DOMAIN}/inboxes/{INBOX}/messages/{message_id}/attachments', headers=headers)
# json_data = response.json()

# # JSON Data
# print(json.dumps(json_data, indent=4))

# attachment = json_data['attachments'][0]
# attachment_id = attachment['attachment-id']
# attachment_filename = attachment['filename']

# # Fetch Attachment
# ######################
# # https://manybrain.github.io/m8rdocs/#fetch-list-of-attachments


# response = requests.get(f'https://mailinator.com/api/v2/domains/{DOMAIN}/inboxes/{INBOX}/messages/{message_id}/attachments/{attachment_id}', headers=headers)
# # print(" ", response.content)
# # json_data = json.loads(response.text)

# with open(attachment_filename, 'wb') as f:
#     for chunk in response.iter_content(chunk_size=1024): 
#         if chunk: # filter out keep-alive new chunks
#             f.write(chunk)

# # JSON Data
# #print(json.dumps(json_data, indent=4))
# print(response.status_code)



# Inject message
######################
# https://manybrain.github.io/m8rdocs/?shell#inject-a-message-http-post-messages


# body = {
#     "from":"storrellas@gmail.com", 
#     "subject":"testing message", 
#     "to": "test1",
#     "parts": [
#         {
#             "headers": {
#                 "content-type": "text/plain; charset=\"UTF-8\""
#             },
#             "body": "here is our test email\r\n"
#         },
#     ]
#   }





# print( "DOMAIN ", DOMAIN )
# print( "INBOX  -> ", INBOX )


# response = requests.post(f'https://mailinator.com/api/v2/domains/{DOMAIN}/inboxes/{INBOX}', \
#                         json = body, headers = headers)
# print("status_code ", response.status_code)
# print("text '", response.text, "'")
# print(response.json())


