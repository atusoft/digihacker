from smtplib import SMTP_SSL


def prompt(prompt):
    return input(prompt).strip()


def send_mail(fromaddr, toaddrs, subject, body):
    # Add the From: and To: headers at the start!
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\n\n%s"
           % (fromaddr, ", ".join(toaddrs), subject, body))
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            break
        msg = msg + line
    print("Message length is", len(msg))
    server = SMTP_SSL('smtp.qq.com')
    server.set_debuglevel(1)
    server.login("atu0830@qq.com", "kiewghebimnpbgjg")
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


if __name__ == '__main__':
    fromaddr = prompt("From: ")
    toaddrs = prompt("To: ").split()
    print("Enter message, end with ^D (Unix) or ^Z (Windows):")
    subject = prompt("Subject: ")
    body = prompt("Body: ")

    send_mail(fromaddr, toaddrs, subject, body)
