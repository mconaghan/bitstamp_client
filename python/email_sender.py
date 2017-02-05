import smtplib
from email.mime.text import MIMEText

class EmailSender:
  
  def __init__(self):
    pass

  def send_email(self, subject, recipient, contents, from_email_addr = "BitstampEmailer@no-reply.com"):

    msg = MIMEText(contents)
    msg['Subject'] = subject
    msg['From']    = from_email_addr
    msg['To']      = recipient

    s = smtplib.SMTP('localhost')
    s.sendmail(from_email_addr, [recipient], msg.as_string())
    s.quit()
