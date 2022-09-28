import smtplib
from email.mime.text import MIMEText
from email.header import Header


class MailBox:

    def __init__(self, smtp_server, sender_account, sender_passwd, myLogger):
        self.smtp_server = smtp_server
        self.sender_account = sender_account
        self.sender_passwd = sender_passwd
        self.myLogegr = myLogger

    def connServer(self):
        try:
            smtp = smtplib.SMTP()
            smtp.connect(self.smtp_server)
            smtp.login(self.sender_account, self.sender_passwd)
            self.smtp = smtp
        except smtplib.SMTPException:
            self.myLogegr.info('邮箱登录失败')
            smtp.quit()

    def connServerBySSL(self):
        try:
            smtp = smtplib.SMTP_SSL(self.smtp_server, 465)
            smtp.login(self.sender_account, self.sender_passwd)
            self.smtp = smtp
        except smtplib.SMTPException:
            self.myLogegr.info('邮箱登录失败')
            smtp.quit()

    def sendMessage(self, sender_addr, receiver_addr, subject, content):
        smtp = self.smtp
        msg = MIMEText(content)
        msg['From'] = '\"打卡提示机器人\" <' + sender_addr + '>'
        msg['To'] = '\"老大\" <' + receiver_addr + '>'
        msg['Subject'] = Header(subject, 'utf-8')
        try:
            smtp.sendmail(sender_addr, receiver_addr, msg.as_string())
        except smtplib.SMTPException:
            self.myLogegr.info('邮件发送失败')
        finally:
            smtp.quit()
