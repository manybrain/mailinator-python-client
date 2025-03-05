import random
import smtplib
import string
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

# def send_mail(send_from, send_to, subject, text, files=None):
#     assert isinstance(send_to, list)

#     # Generate message
#     msg = MIMEMultipart()
#     msg['From'] = send_from
#     msg['To'] = COMMASPACE.join(send_to)
#     msg['Date'] = formatdate(localtime=True)
#     msg['Subject'] = subject
#     msg.attach(MIMEText(text))

#     # Attach files
#     for f in files or []:
#         with open(f, "rb") as fil:
#             part = MIMEApplication(
#                 fil.read(),
#                 Name=basename(f)
#             )
#         # After the file is closed
#         part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
#         msg.attach(part)


#     # Initiate SMTP lib
#     smtp = smtplib.SMTP()

#     smtp.connect(SMTP_SERVER, SMTP_PORT)
#     # identify ourselves to smtp gmail client
#     smtp.ehlo()
#     # secure our email with tls encryption
#     smtp.starttls()
#     # re-identify ourselves as an encrypted connection
#     smtp.ehlo()
#     smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
#     # Send the actual email
#     response = smtp.sendmail(send_from, send_to, msg.as_string())
#     print(response)
#     # Close SMTP connection
#     smtp.close()

        

class TestClass:

    mailinator = Mailinator(API_TOKEN)
    mailinator_without_api_token = Mailinator()

    def test_authenticators(self):
        logger.info("+++ test_authenticators +++")

        # InstantTOTP2FACode
        print("Instant TOTP 2FA Code ...")
        codes = self.mailinator.request( InstantTOTP2FACodeRequest(AUTH_SECRET) )
        print("codes ", codes)
        print("DONE!")
        
        # GetAuthenticatorsRequest
        print("Get Authenticators ...")
        codes = self.mailinator.request( GetAuthenticatorsRequest() )
        print("codes ", codes)
        print("DONE!")
        
        # GetAuthenticatorsByIdRequest
        print("Get Authenticators By Id ...")
        codes = self.mailinator.request( GetAuthenticatorsByIdRequest(AUTH_ID) )
        print("codes ", codes)
        print("DONE!")
        
        # GetAuthenticatorRequest
        print("Get Authenticator ...")
        codes = self.mailinator.request( GetAuthenticatorRequest() )
        print("codes ", codes)
        print("DONE!")
        
        # GetAuthenticatorByIdRequest
        print("Get Authenticator By Id ...")
        codes = self.mailinator.request( GetAuthenticatorByIdRequest(AUTH_ID) )
        print("codes ", codes)
        print("DONE!")

    def test_fetch_inbox(self):
        logger.info("+++ test_fetch_inbox +++")

        if SEND_EMAIL_ENABLED:
            send_mail(SMTP_SENDER, [f'{INBOX}@{DOMAIN}'], "subject for test", "Here my mail", files='./tintin.jpg')
            print("Sent email. Giving some time to backend ...")
            time.sleep(10)

        # Fetch Inbox
        print("Fetching Inbox ...")
        inbox = self.mailinator.request( GetInboxRequest(DOMAIN, INBOX) )
        assert len(inbox.msgs) == 1        
        print("DONE!")

        # Fetch Inbox With Cursor Param
        print("Fetching Inbox With Cursor Param...")
        inbox = self.mailinator.request( GetInboxRequest(DOMAIN, INBOX, cursor=inbox.cursor, limit=1) )
        assert len(inbox.msgs) == 1        
        print("DONE!")

        # Fetch Inbox With Full Param
        print("Fetching Inbox With Full Param...")
        inbox = self.mailinator.request( GetInboxRequest(DOMAIN, INBOX, full=true, limit=1) )
        assert len(inbox.msgs) == 1        
        print("DONE!")
        
        # Fetch Inbox With Delete Param
        print("Fetching Inbox With Delete Param...")
        inbox = self.mailinator.request( GetInboxRequest(DOMAIN, INBOX, delete="10s", limit=1) )
        assert len(inbox.msgs) == 1        
        print("DONE!")
        
        # Fetch Inbox With Wait Param
        print("Fetching Inbox With Wait Param...")
        inbox = self.mailinator.request( GetInboxRequest(DOMAIN, INBOX, wait="10s", limit=1) )
        assert len(inbox.msgs) == 1        
        print("DONE!")

        # Get message_id
        message_id = inbox.msgs[0].id
        print("Message id ", message_id)

        # Get Inbox Message
        print("Fetching Message ...")
        message = self.mailinator.request( GetInboxMessageRequest(DOMAIN, INBOX, message_id) )
        print("DONE!")

        # Get Message
        print("Fetching Message ...")
        message = self.mailinator.request( GetMessageRequest(DOMAIN, message_id) )
        print("DONE!")

        # Get Message With Delete Param
        print("Fetching Message With Delete Param ...")
        message = self.mailinator.request( GetMessageRequest(DOMAIN, message_id, "10s") )
        print("DONE!")

        # Get Inbox Message Attachments list
        print("Fetching Inbox Message Attachments ...")
        attachments = self.mailinator.request( GetInboxMessageAttachmentsRequest(DOMAIN, INBOX, MESSAGE_WITH_ATTACHMENT_ID) )
        assert len(inbox.msgs) == 1
        print("DONE!")

        # Get Message Attachments list
        print("Fetching Message Attachments ...")
        attachments = self.mailinator.request( GetMessageAttachmentsRequest(DOMAIN, MESSAGE_WITH_ATTACHMENT_ID) )
        assert len(inbox.msgs) == 1
        print("DONE!")

        # Get attachment_id
        attachment = attachments.attachments[0]
        attachment_id = attachment.attachment_id
        attachment_filename = attachment.filename
        print("Attachment Id ", attachment_id)

        # Get Inbox Message Attachment
        response = self.mailinator.request( GetInboxMessageAttachmentRequest(DOMAIN, INBOX, message_id, MESSAGE_WITH_ATTACHMENT_ID) )

        # Print out attachment
        output_filepath = 'downloaded_' + attachment_filename
        with open(output_filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

        # Get Message Attachment
        response = self.mailinator.request( GetMessageAttachmentRequest(DOMAIN, message_id, MESSAGE_WITH_ATTACHMENT_ID) )

        # Print out attachment
        output_filepath = 'downloaded_' + attachment_filename
        with open(output_filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

        # Get Message links
        print("Fetching Links ...")
        links = self.mailinator.request( GetMessageLinksRequest(DOMAIN, message_id) )
        print("links ", links )
        print("DONE!")

        Get Message links full
        print("Fetching Links Full...")
        linksFull = self.mailinator.request( GetMessageLinksFullRequest(DOMAIN, message_id) )
        print("links full ", linksFull )
        print("DONE!")

        # Get Inbox Message links
        print("Fetching Inbox Message Links ...")
        links = self.mailinator.request( GetInboxMessageLinksRequest(DOMAIN, INBOX, message_id) )
        print("links ", links )
        print("DONE!")

        # Post Message
        print("Post Message ...")
        post_message = PostMessage({'from':'sergi@mail.com', 'subejct': "here my subject", 'text':"hello"})
        response = self.mailinator.request( PostMessageRequest(DOMAIN, INBOX, post_message) )
        print(response)
        print("DONE!")

        # Get Inbox Message Smtp Log
        print("Fetching Inbox Message Smtp Log ...")
        smtp_log = self.mailinator.request( GetInboxMessageSmtpLogRequest(DOMAIN, INBOX, message_id) )
        print("smtp log ", smtp_log )
        print("DONE!")
        
        # Get Message Smtp Log
        print("Fetching Message Smtp Log ...")
        smtp_log = self.mailinator.request( GetMessageSmtpLogRequest(DOMAIN, message_id) )
        print("smtp log ", smtp_log )
        print("DONE!")

        # Get Inbox Message Raw
        print("Fetching Inbox Message Raw ...")
        raw_data = self.mailinator.request( GetInboxMessageRawRequest(DOMAIN, INBOX, message_id) )
        print("raw data ", raw_data )
        print("DONE!")

        # Get Message Raw
        print("Fetching Message Raw ...")
        raw_data = self.mailinator.request( GetMessageRawRequest(DOMAIN, message_id) )
        print("raw data ", raw_data )
        print("DONE!")

        # Get Latest Inbox Messages
        print("Fetching Latest Inbox Messages ...")
        latest_messages = self.mailinator.request( GetLatestInboxMessagesRequest(DOMAIN, INBOX) )
        print("latest messages ", latest_messages )
        print("DONE!")

        # Get Latest Messages
        print("Fetching Latest Messages ...")
        latest_messages = self.mailinator.request( GetLatestMessagesRequest(DOMAIN) )
        print("latest messages ", latest_messages )
        print("DONE!")

        # Delete Message Request
        if DELETE_REQUESTS:
            response = self.mailinator.request( DeleteDomainMessagesRequest(DOMAIN) )
            response = self.mailinator.request( DeleteInboxMessagesRequest(DOMAIN) )        
            response = self.mailinator.request( DeleteMessageRequest(DOMAIN, INBOX, message_id) )


    def test_fetch_sms_inbox(self):
        logger.info("+++ test_fetch_sms_inbox +++")

        # Fetch Inbox
        print("Fetching SMS Inbox ...")
        inbox = self.mailinator.request( GetSmsInboxRequest(SMS_DOMAIN, SMS_PHONE_NUMBER) )
        print("inbox ", inbox)        
        print("DONE!")


    def test_domains(self):
        logger.info("+++ test_domains +++")

        # Get domains
        print("Fetching Domains ...")
        domains = self.mailinator.request( GetDomainsRequest() )
        print("domains ", domains)
        print("DONE!")

      
        # Get domain
        print("Fetching Domain ...")
        domain = self.mailinator.request( GetDomainRequest(DOMAIN) )
        print("domain ", domain.to_json())
        print("DONE!")
        
        domainNameToCreate = "testpython.testinator.com" 

        # Create domain
        print("Create Domain ...")
        status = self.mailinator.request( CreateDomainRequest(domainNameToCreate) )
        print("DONE!")

        # Delete domain
        print("Delete Domain ...")
        status = self.mailinator.request( DeleteDomainRequest(domainNameToCreate) )
        print("DONE!")


    def test_rules(self):
        logger.info("+++ test_rules +++")

        # Create Rule
        conditions = [Condition(operation=Condition.OperationType.PREFIX, field="to", value="test")]
        actions = [Action(action=Action.ActionType.DROP, action_data=Action.ActionData("https://www.mywebsite.com/restendpoint"))]
        random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))  # Generate a random string of length 8
        rule = Rule(description="mydescription", enabled=True, name=f"RuleNameFromPythonTest_{random_suffix}", conditions=conditions, actions=actions)

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


    def test_webhooks(self):
        logger.info("+++ test_webhooks +++")

        webhook = Webhook(_from="MyMailinatorPythonTest", subject="testing message", text="hello world", to="jack")

        # Private Webhook
        print("Private Webhook ...")
        webhook_response = self.mailinator_without_api_token.request( PrivateWebhookRequest(WEBHOOKTOKEN_PRIVATEDOMAIN, webhook) )
        print("DONE!") 
        
        # Private Inbox Webhook
        print("Private Inbox Webhook ...")
        webhook_response = self.mailinator_without_api_token.request( PrivateInboxWebhookRequest(WEBHOOKTOKEN_PRIVATEDOMAIN, WEBHOOK_INBOX, webhook) )
        print("DONE!") 
        
        # Private Custom Service Webhook
        print("Private Custom Service Webhook ...")
        webhook_response = self.mailinator_without_api_token.request( PrivateCustomServiceWebhookRequest(WEBHOOKTOKEN_CUSTOMSERVICE, WEBHOOK_CUSTOMSERVICE, webhook) )
        print("DONE!") 
        
        # Private Custom Service Inbox Webhook
        print("Private Custom Service Inbox Webhook ...")
        webhook_response = self.mailinator_without_api_token.request( PrivateCustomServiceInboxWebhookRequest(WEBHOOKTOKEN_CUSTOMSERVICE, WEBHOOK_CUSTOMSERVICE, WEBHOOK_INBOX, webhook) )
        print("DONE!") 

    def test_stats(self):
        logger.info("+++ test_stats +++")

        # Get team
        print("Fetching Team ...")
        team = self.mailinator.request( GetTeamRequest() )
        print("team ", team)
        print("DONE!")

        # Get stats
        print("Fetching Team Stats ...")
        team = self.mailinator.request( GetTeamStatsRequest() )
        print("team stats ", team)
        print("DONE!")
        
        # Get team info
        print("Fetching Team Info ...")
        team = self.mailinator.request( GetTeamInfoRequest() )
        print("team info ", team)
        print("DONE!")
