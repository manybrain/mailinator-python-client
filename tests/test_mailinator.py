import smtplib
import requests
import time
import json
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


# Project includes
from mailinator import *
from utils import get_logger
logger = get_logger()


# Import localsettings if any
try:
    from localsettings import *
except ImportError:
    pass


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

    # @classmethod
    # def setup_class(cls):
    #     logger.info(f"Clearing all inbo messages for domain {DOMAIN} ...")

    #     # Delete all msgs from domain
    #     mailinator = Mailinator(API_TOKEN, INBOX, DOMAIN)
    #     response = mailinator.delete_domain()

    #     # Fetch Inbox
    #     response = mailinator.fetch_inbox()
    #     print(response)
    #     assert len( response['msgs'] ) == 0
    #     logger.info(f"DONE!")



    # @classmethod
    # def teardown_class(cls):
    #     print("starting class: {} execution".format(cls.__name__))
    #     logger.info("END ---->")


    # def setup(self):
    #     logger.info(f"Clearing all inbox messages for domain {DOMAIN} ...")

    #     # Delete all msgs from domain
    #     mailinator = Mailinator(API_TOKEN, DOMAIN)
    #     response = mailinator.delete_domain()

    #     # Fetch Inbox
    #     response = mailinator.fetch_inbox(INBOX)
    #     print(response)
    #     assert len(response['msgs']) == 0
    #     logger.info(f"DONE!")

    def test_fetch_inbox(self):
        logger.info("+++ test_fetch_inbox +++")

        # Fetch Inbox
        inbox = self.mailinator.request( GetInboxRequest(DOMAIN, INBOX) )
        assert len(inbox.msgs) == 1

        print( "inbox ", inbox )
        print( "inbox ", inbox.msgs[0] )

        # Get message_id
        message_id = inbox.msgs[0].id

        # Get Message
        message = self.mailinator.request( GetMessageRequest(DOMAIN, INBOX, message_id) )

        # Get Attachements list
        attachments = self.mailinator.request( GetAttachmentsRequest(DOMAIN, INBOX, message_id) )
        print("attachments ", attachments)

        # Get attachment_id
        attachment = attachments.attachments[0]
        attachment_id = attachment.attachment_id
        attachment_filename = attachment.filename

        # Get Attachement
        response = self.mailinator.request( GetAttachmentRequest(DOMAIN, INBOX, message_id, attachment_id) )

        # Print out attachment
        output_filepath = 'downloaded_' + attachment_filename
        with open(output_filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)


        # Delete Message Request
        response = self.mailinator.request( DeleteDomainMessagesRequest(DOMAIN) )
        # response = self.mailinator.request( DeleteInboxMessagesRequest(DOMAIN) )        
        # response = self.mailinator.request( DeleteMessageRequest(DOMAIN, INBOX, message_id) )



    def test_fetch_sms_inbox(self):
        logger.info("+++ test_fetch_sms_inbox +++")

        # Fetch Inbox
        inbox = self.mailinator.request( GetSmsInboxRequest(SMS_DOMAIN, SMS_PHONE_NUMBER) )
        print("inbox ", inbox)
        print("inbox ", inbox.to_json() )


    def test_domains(self):
        logger.info("+++ test_domains +++")

        # Get doamins
        domains = self.mailinator.request( GetDomainsRequest() )
        print("domains ", domains)
        print("domain ", domains.to_json())

        # # Generate model
        # #domains = Domains(domains= [Domain(**k) for k in response['domains'] ])
        # domains = Domains(**response)
      
        # Get doamins
        domain = self.mailinator.request( GetDomainRequest(DOMAIN) )
        print("domain ", domain.to_json())

        # # Output results
        # results_json = json.dumps(response, indent=2)
        # #print(json.dumps(results, indent=2))
        # print(results_json)

        # # Generate model
        # domain = Domain(**response)

        # print("Domain ", domain)



    def test_rules(self):
        logger.info("+++ test_rules +++")

        # Create Rule
        conditions = [Condition(operation=Condition.OperationType.PREFIX, field="to", value="test")]
        actions = [Action(action=Action.ActionType.DROP, action_data=Action.ActionData("https://www.mywebsite.com/restendpoint"))]
        rule = Rule(description="mydescription", enabled=True, name="MyName", conditions=conditions, actions=actions)

        rule = self.mailinator.request( CreateRuleRequest(DOMAIN, rule ) )
        print("rule ", rule)

        # Get all Rules
        rules = self.mailinator.request( GetRulesRequest(DOMAIN) )

        # Get rule_id
        rule_id = rules.rules[0]._id

        # Get rule
        rule = self.mailinator.request( GetRuleRequest(DOMAIN, rule_id) )
        rule_id = rules.rules[0]._id

        # Enable Rule
        self.mailinator.request( EnableRuleRequest(DOMAIN, rule_id) )

        # Disable Rule
        self.mailinator.request( DisableRuleRequest(DOMAIN, rule_id) )

        # Delete Rule
        response = self.mailinator.request( DeleteRuleRequest(DOMAIN, rule_id) )
        print(response)
