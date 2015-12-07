# -*- encoding utf-8 -*-
import smtplib
from email import MIMEText as mimetext
#from email.mime.multipart import MIMEMultipart as multipart
from email import MIMEMultipart as multipart
import SdeArchivistProperties

class MailSender:
    """
    Enables sending emails to a assigned user
    """

    def __init__(self, properties):
        self.__props = properties
        print self.__props["port"]
        #only ascii for the server and port
        self.__smtpObj = smtplib.SMTP(str(self.__props["smtp_server"]),str(self.__props["port"]))
        self.__smtpObj.starttls()

    def send(self, to, content):
        self.__smtpObj.login(self.__props["username"], self.__props["password"])
        msg = multipart.MIMEMultipart()
        from_addr = self.__props["from"]
        msg["FROM"] = from_addr
        tos_addr = [to]
        tos_addr.extend(self.__props["additional_recipients"])
        msg["TO"] = to;
        msg["Subject"] = self.__props["subject"]

        body = self.__props["failure_message"]
        body += "\n\n" + content

        msg.attach(mimetext.MIMEText(body, "plain"))

        self.__smtpObj.sendmail("patrick.hebner@ufz.de", tos_addr, msg.as_string());
        self.__smtpObj.quit()

if __name__ == "__main__":
    props = SdeArchivistProperties.SdeArchivistProperties("config/archivist_config.json").mail_config
    m = MailSender(props)
    m.send("patrick.hebner@ufz.de", "TEST CONTENT")