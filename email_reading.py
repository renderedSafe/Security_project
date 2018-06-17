import email
import imaplib
import cv2
import numpy as np
from datetime import datetime


class EmailMessage:
    def __init__(self, message_body=None, attached_image=None, timestamp=None):
        self.message_body = message_body
        self.attached_image = attached_image
        self.timestamp = timestamp

    def get_image_object(self):
        '''

        :return: numpy.array of the image
        '''
        np_bytes = np.fromstring(self.attached_image, np.uint8)
        image_np = cv2.imdecode(np_bytes, cv2.IMREAD_ANYCOLOR)
        return image_np


class EmailScraper:
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

        self.imap_session = imaplib.IMAP4_SSL('imap.gmail.com')
        self.typ, self.account_details = self.imap_session.login(self.username, self.password)
        if self.typ != 'OK':
            print('Not able to sign in!')

        self.imap_session.select('INBOX')

        self.last_message_timestamp = datetime.now()

    def get_newest_message(self, subject='Alarm Message'):
        typ, data = self.imap_session.search(None, f'(SUBJECT "{subject}")')
        if typ != 'OK':
            print('Error searching Inbox.')
        else:
            try:
                msg_id = data[0].split()[0]
                typ, message_parts = self.imap_session.fetch(msg_id, '(RFC822)')
                if typ != 'OK':
                    print('Error fetching mail.')
                else:
                    email_body = message_parts[0][1]
                    mail = email.message_from_bytes(email_body)
                    timestamp = None
                    body = None
                    image = None
                    for part in mail.walk():
                        filename = part.get_filename()
                        if filename:
                            image = part.get_payload(decode=True)

            except IndexError:
                print('No new emails matching criteria.')
        try:
            return EmailMessage(body, image, timestamp)
        except Exception as e:
            print(e)
