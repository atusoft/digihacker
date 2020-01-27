import email
import ssl
from imapclient import IMAPClient

from emailClient.utils import Settings

settings = Settings()
ssl_context = ssl.create_default_context()

# don't check if certificate hostname doesn't match target hostname
ssl_context.check_hostname = False

# don't check if the certificate is truste
ssl_context.verify_mode = ssl.CERT_NONE
with IMAPClient(settings.imap_server,ssl_context=ssl_context) as server:
    server.login(settings.user['name'], settings.user['password'])
    server.select_folder('INBOX', readonly=True)

    messages = server.search('UNSEEN')
    for uid, message_data in server.fetch(messages, 'RFC822').items():
        email_message = email.message_from_bytes(message_data[b'RFC822'])
        print(uid, email_message.get('From'), email_message.get('Subject'))
