import quopri
import re
from imaplib import IMAP4_SSL
import email
import arrow

from bs4 import BeautifulSoup as bs
import base64
import yaml


def encoded_words_to_text(encoded_words):
    """ from https://dmorgan.info/posts/encoded-word-syntax/  """
    if not encoded_words.startswith("=?"):
        return encoded_words
    encoded_word_regex = r'=\?{1}(.+)\?{1}([B|Q])\?{1}(.+)\?{1}='
    charset, encoding, encoded_text = re.match(encoded_word_regex, encoded_words, flags=re.IGNORECASE).groups()
    if encoding.upper() == 'B':
        byte_string = base64.b64decode(encoded_text)
    elif encoding.upper() == 'Q':
        byte_string = quopri.decodestring(encoded_text)
    return byte_string.decode(charset)


def parseHeader(message):
    """ 解析邮件首部 """
    try:
        subject = message.get('Subject')
        # subject=str(message)
        # if subject is not None:
        h = email.header.Header(subject, charset='utf-8')
        dh = email.header.decode_header(h)
        subject = str(dh[0][0], encoding="utf-8")
        subject = encoded_words_to_text(subject)
        # .encode('utf-8')
        # print(h)
        # # 发件人
        from_sb = encoded_words_to_text(email.utils.parseaddr(message.get('from'))[0])
        if len(from_sb) == 0:
            from_sb = encoded_words_to_text(email.utils.parseaddr(message.get('from'))[1])
        # # 收件人
        to_sb = email.utils.parseaddr(message.get('to'))[1]
        # # 抄送人
        cc = email.utils.parseaddr(message.get_all('cc'))[1]
        # try:
        fmt = "ddd, D MMM YYYY HH:mm:ss Z"

        # date = arrow.get(message['Date'], fmt)
        date = arrow.get(message['Received'].split(';')[1], fmt)

        print(f"{from_sb:30} {subject:80} {date.humanize():20}")
    except Exception as e:
        print(e)
        print(f"happen on {message['Received'].split(';')[1]}")


def parseBody(message):
    for part in message.walk():
        if not part.is_multipart():
            charset = part.get_charset()
            contenttype = part.get_content_type()
            name = part.get_param("name")
            if name:
                fh = email.header.Header(name)
                fdh = email.header.decode_header(fh)
                fname = fdh[0][0]
                print('附件名:', fname)
            else:
                # 不是附件，是文本内容
                html = bs(part.get_payload(decode=True), features="lxml")
                for script in html(["script", "style"]):  # remove all javascript and stylesheet code
                    script.decompose()
                text = html.get_text()

                # break into lines and remove leading and trailing space on each
                lines = (line.strip() for line in text.splitlines())
                # break multi-headlines into a line each
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # drop blank lines
                text = '\n'.join(chunk for chunk in chunks if chunk)

                print(text)


def show_all(M):
    try:
        # search_criteria = '[REVERSE] DATE'  # Ascending, most recent email last
        typ, data = M.search(None, '(UNSEEN)')
        # typ, data = M.sort(search_criteria, 'UTF-8', 'ALL')
        count = 10
        pcount = 1
        for num in data[0].split():
            typ, data = M.fetch(num, '(RFC822)')
            for response_part in data:
                print(data)
                if isinstance(response_part, tuple):
                    part = response_part[1].decode('utf-8')
                    msg = email.message_from_string(part)
                    parseHeader(msg)
                    # parseBody(msg)
            pcount += 1
            if pcount > count:
                break
    except Exception as e:
        print(e)


def choose_folder(name='INBOX'):
    M.select(name)


if __name__ == '__main__':
    with open('settings.yml') as f:
        settings = yaml.safe_load(f)
    with IMAP4_SSL(settings['imap_server']) as M:
        M.noop()
        user = settings['user']
        M.login(user['name'], user['password'])
        M.select()
        show_all(M)
        M.close()
        M.logout()
