import smtplib
import requests
import time
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


        # Send email
        ##
        # send_mail('storrellas@gmail.com', ['test1@storrellasteam.m8r.co'], \
        #             'MySubject', 'Here my text')
        # # Wait three secs until email is processed
        # time.sleep(6)

        # Fetch Inbox
        response = self.mailinator.fetch_inbox(DOMAIN, INBOX)
        print(response)
        assert len(response['msgs']) == 1

        # Get message_id
        message = response['msgs'][0]
        message_id = message['id']


        # Fetch message
        response = self.mailinator.fetch_message(DOMAIN, INBOX, message_id)
        print(response['origfrom'])

        # Fetch message list attachments
        response = self.mailinator.fetch_message_list_attachments(DOMAIN, INBOX, message_id)
        print(response)

        # Get attachment_id
        attachment = response['attachments'][0]
        attachment_id = attachment['attachment-id']
        attachment_filename = attachment['filename']

        # Fetch message list attachments
        response = self.mailinator.fetch_message_attachment(DOMAIN, INBOX, message_id, \
                                                    attachment_id, './tintin_output.jpg')
        print(response)

        # Delete inbox for user
        # self.mailinator.delete_message(DOMAIN, INBOX, message_id)
        # self.mailinator.delete_inbox(DOMAIN, INBOX)
        # self.mailinator.delete_domain(DOMAIN)


    def test_fetch_sms_inbox(self):
        logger.info("+++ test_fetch_sms_inbox +++")

        # Fetch SMS Message
        SMS_INBOX = 'public'
        SMS_TEAM_NUMBER = '12013814330'

        # Get SMS INBOX
        response = self.mailinator.fetch_sms_inbox(SMS_INBOX, SMS_TEAM_NUMBER)
        print(response)


    def test_domains(self):
        logger.info("+++ test_domains +++")

        # Domain id
        response = self.mailinator.get_all_domains()
        print(response)

        # Get domain_id
        domain = response['domains'][0]
        domain_id = domain['_id']
        
        response = self.mailinator.get_domain(domain_id)
        print(response)


    def test_rules(self):
        logger.info("+++ test_rules +++")

        # Create Rule
        data = {
            "description": "Rule to post all incoming mail starting with test* to my webhook",
            "enabled": True,
            "name": "testprefixpost",
            "conditions": [
                {
                    "operation": "PREFIX",
                    "condition_data": {
                        "field": "to",
                        "value": "test"
                    }
                }
            ],
            "actions": [
                {
                    "action": "WEBHOOK",
                    "action_data": {
                        "url": "https://www.mywebsite.com/restendpoint"
                    }
                }
            ]
        }
        response = self.mailinator.create_rule(DOMAIN, data)
        print(response)

        # Get all Rules
        response = self.mailinator.get_all_rules(DOMAIN)

        # Get rule_id
        rule = response['rules'][0]
        rule_id = rule['_id']

        # Get rule
        response = self.mailinator.get_rule(DOMAIN, rule_id)
        print(response)

        # Enable Rule
        assert self.mailinator.enable_rule(DOMAIN, rule_id) == True

        # Disable Rule
        assert self.mailinator.disable_rule(DOMAIN, rule_id) == True

        # Delete Rule
        response = self.mailinator.delete_rule(DOMAIN, rule_id)
        print(response)
