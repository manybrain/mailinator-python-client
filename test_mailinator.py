import smtplib
import requests
import time
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


# Project includes
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


class Mailinator:

    token = None
    domain = None

    __headers = {}
    __base_url = 'https://mailinator.com/api/v2'

    def __init__(self, token, domain):
        self.domain = domain
        self.token = token
        if self.token is None:
            raise ValueError('Token cannot be None')

        self.headers = {'Authorization': self.token}

    def fetch_inbox(self, inbox):
        if inbox is None:
            raise ValueError('Token cannot be None')
        url=f'{self.__base_url}/domains/{self.domain}/inboxes/{inbox}?limit=2&sort=descending'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def fetch_message(self, inbox, message_id):
        if inbox is None:
            raise ValueError('inbox cannot be None')
        if message_id is None:
            raise ValueError('inbox cannot be None')

        url=f'{self.__base_url}/domains/{self.domain}/inboxes/{inbox}/messages/{message_id}'
        response = requests.get(url, headers=self.headers)
        return response.json()


    def fetch_sms_inbox(self, sms_inbox, sms_team_number):
        if sms_inbox is None:
            raise ValueError('sms_inbox cannot be None')
        if sms_team_number is None:
            raise ValueError('sms_team_member cannot be None')

        url=f'{self.__base_url}/domains/{sms_inbox}/inboxes/{sms_team_number}'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def fetch_message_list_attachments(self, inbox, message_id):
        if inbox is None:
            raise ValueError('inbox cannot be None')
        if message_id is None:
            raise ValueError('inbox cannot be None')

        url=f'{self.__base_url}/domains/{self.domain}/inboxes/{inbox}/messages/{message_id}/attachments'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def fetch_message_attachment(self, inbox, message_id, attachment_id, output_filename):
        url=f'https://mailinator.com/api/v2/domains/{DOMAIN}/inboxes/{INBOX}/messages/{message_id}/attachments/{attachment_id}'
        response = requests.get(url, headers=self.headers)
        # print(" ", response.content)
        # json_data = json.loads(response.text)

        with open(output_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    def delete_inbox(self, inbox):
        if inbox is None:
            raise ValueError('INBOX cannot be None')
        # Delete inbox
        requests.delete(f'https://mailinator.com/api/v2/domains/{self.domain}/inboxes/{inbox}', headers=self.headers)


    def delete_domain(self):
        requests.delete(f'https://mailinator.com/api/v2/domains/{self.domain}/inboxes', headers=self.headers)

        

class TestClass:

    mailinator = Mailinator(API_TOKEN, DOMAIN)

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
        response = self.mailinator.fetch_inbox(INBOX)
        print(response)
        assert len(response['msgs']) == 1

        # Get message_id
        message = response['msgs'][0]
        message_id = message['id']


        # Fetch message
        response = self.mailinator.fetch_message(INBOX, message_id)
        print(response['origfrom'])

        # Fetch message list attachments
        response = self.mailinator.fetch_message_list_attachments(INBOX, message_id)
        print(response)

        # Get attachment_id
        attachment = response['attachments'][0]
        attachment_id = attachment['attachment-id']
        attachment_filename = attachment['filename']

        # Fetch message list attachments
        response = self.mailinator.fetch_message_attachment(INBOX, message_id, \
                                                    attachment_id, './tintin_output.jpg')
        print(response)


    # def test_fetch_sms_inbox(self):
    #     logger.info("+++ test_fetch_sms_inbox +++")

    #     # Fetch SMS Message
    #     SMS_INBOX = 'public'
    #     SMS_TEAM_NUMBER = '12013814330'

    #     # Get SMS INBOX
    #     response = self.mailinator.fetch_sms_inbox(SMS_INBOX, SMS_TEAM_NUMBER)
    #     print(response)

    #     # # Delete inbox for user
    #     # response = self.mailinator.delete_inbox(INBOX)

    #     # # Check inbox is empty
    #     # response = self.mailinator.fetch_inbox(INBOX)
    #     # assert len(response['msgs']) == 0

    # # def test_delete_domain(self):
    # #     logger.info("+++ test_delete_domain +++")

    # #     # Send email
    # #     ##
    # #     send_mail('sergi@mail.com', ['user1@storrellasteam.m8r.co'], \
    # #                 'MySubject', 'Here my text')
    # #     send_mail('sergi@mail.com', ['user2@storrellasteam.m8r.co'], \
    # #                 'MySubject', 'Here my text')                    
    # #     # Wait three secs until email is processed
    # #     time.sleep(3)

    # #     # Fetch Inbox
    # #     response = self.mailinator.fetch_inbox(INBOX)
    # #     assert len(response['msgs']) == 2