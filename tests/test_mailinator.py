import smtplib
import requests
import time
import json
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import sys


# Project includes
from mailinator import *
from utils import get_logger
logger = get_logger()


# Import localsettings if any
try:
    from .localsettings import *
except ImportError:
    pass


try: DELETE_REQUESTS
except: 
    print("Remember to copy the localsettings file!")
    sys.exit(0)

def send_mail(send_from, send_to, subject, text, files=None):
    assert isinstance(send_to, list)

    # Generate message
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    # Attach files
    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)


    # Initiate SMTP lib
    smtp = smtplib.SMTP()

    smtp.connect(SMTP_SERVER, SMTP_PORT)
    # identify ourselves to smtp gmail client
    smtp.ehlo()
    # secure our email with tls encryption
    smtp.starttls()
    # re-identify ourselves as an encrypted connection
    smtp.ehlo()
    smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
    # Send the actual email
    response = smtp.sendmail(send_from, send_to, msg.as_string())
    print(response)
    # Close SMTP connection
    smtp.close()

        

class TestClass:

    mailinator = Mailinator(API_TOKEN)


    def test_fetch_inbox(self):
        logger.info("+++ test_fetch_inbox +++")

        # if SEND_EMAIL_ENABLED:
        #     send_mail(SMTP_SENDER, [f'{INBOX}@{DOMAIN}'], "subject for test", "Here my mail", files='./tintin.jpg')
        #     print("Sent email. Giving some time to backend ...")
        #     time.sleep(10)

        # # Fetch Inbox
        # print("Fetching Inbox ...")
        # inbox = self.mailinator.request( GetInboxRequest(DOMAIN, INBOX) )
        # assert len(inbox.msgs) == 1        
        # print("DONE!")

        # # Get message_id
        # message_id = inbox.msgs[0].id
        # print("Message id ", message_id)

        # # Get Message
        # print("Fetching Message ...")
        # message = self.mailinator.request( GetMessageRequest(DOMAIN, INBOX, message_id) )
        # print("DONE!")

        # # Get Attachements list
        # print("Fetching Attachments ...")
        # attachments = self.mailinator.request( GetAttachmentsRequest(DOMAIN, INBOX, message_id) )
        # assert len(inbox.msgs) == 1
        # print("DONE!")

        # # Get attachment_id
        # attachment = attachments.attachments[0]
        # attachment_id = attachment.attachment_id
        # attachment_filename = attachment.filename
        # print("Attachment Id ", attachment_id)

        # # Get Attachement
        # response = self.mailinator.request( GetAttachmentRequest(DOMAIN, INBOX, message_id, attachment_id) )

        # # Print out attachment
        # output_filepath = 'downloaded_' + attachment_filename
        # with open(output_filepath, 'wb') as f:
        #     for chunk in response.iter_content(chunk_size=1024): 
        #         if chunk: # filter out keep-alive new chunks
        #             f.write(chunk)

        # # Get Message links
        # print("Fetching Links ...")
        # links = self.mailinator.request( GetMessageLinksRequest(DOMAIN, INBOX, message_id) )
        # print("links ", links )
        # print("DONE!")


        # # Delete Message Request
        # if DELETE_REQUESTS:
        #     response = self.mailinator.request( DeleteDomainMessagesRequest(DOMAIN) )
        #     response = self.mailinator.request( DeleteInboxMessagesRequest(DOMAIN) )        
        #     response = self.mailinator.request( DeleteMessageRequest(DOMAIN, INBOX, message_id) )

        post_message = PostMessage({'from':'sergi@mail.com', 'subejct': "here my subject", 'text':"hello"})
        response = self.mailinator.request( PostMessageRequest(DOMAIN, INBOX, post_message) )
        print(response)


    def test_fetch_sms_inbox(self):
        logger.info("+++ test_fetch_sms_inbox +++")

        # Fetch Inbox
        print("Fetching SMS Inbox ...")
        inbox = self.mailinator.request( GetSmsInboxRequest(SMS_DOMAIN, SMS_PHONE_NUMBER) )
        print("inbox ", inbox)        
        print("DONE!")


    def test_domains(self):
        logger.info("+++ test_domains +++")

        # Get doamins
        print("Fetching Domains ...")
        domains = self.mailinator.request( GetDomainsRequest() )
        print("domains ", domains)
        print("DONE!")

      
        # Get doamain
        print("Fetching Domain ...")
        domain = self.mailinator.request( GetDomainRequest(DOMAIN) )
        print("domain ", domain.to_json())
        print("DONE!")


    def test_rules(self):
        logger.info("+++ test_rules +++")

        # Create Rule
        conditions = [Condition(operation=Condition.OperationType.PREFIX, field="to", value="test")]
        actions = [Action(action=Action.ActionType.DROP, action_data=Action.ActionData("https://www.mywebsite.com/restendpoint"))]
        rule = Rule(description="mydescription", enabled=True, name="MyName", conditions=conditions, actions=actions)

        print("Create Rule ...")
        rule = self.mailinator.request( CreateRuleRequest(DOMAIN, rule ) )
        print("DONE!")

        # Get all Rules
        print("Get All Rules ...")
        rules = self.mailinator.request( GetRulesRequest(DOMAIN) )
        print("DONE!")

        # Get rule_id
        rule_id = rules.rules[0]._id

        # Get rule
        print(f'Get Rule {rule_id} ...')
        rule = self.mailinator.request( GetRuleRequest(DOMAIN, rule_id) )
        rule_id = rules.rules[0]._id
        print("DONE!")

        # Enable Rule
        print(f'Enable Rule {rule_id} ...')
        self.mailinator.request( EnableRuleRequest(DOMAIN, rule_id) )
        
        # Disable Rule
        print(f'Disable Rule {rule_id} ...')
        self.mailinator.request( DisableRuleRequest(DOMAIN, rule_id) )
        print("DONE!")

        # Delete Rule
        print(f'Delete Rule {rule_id} ...')
        response = self.mailinator.request( DeleteRuleRequest(DOMAIN, rule_id) )
        print("DONE!")
