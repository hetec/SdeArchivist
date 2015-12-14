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
        #only ascii for the server and port
        self.__smtpObj = smtplib.SMTP(str(self.__props["smtp_server"]), str(self.__props["port"]))
        self.__smtpObj.starttls()

    def send(self, to, content):
        self.__smtpObj.login(self.__props["username"], self.__props["password"])
        tos_addr = [to]
        tos_addr.extend(self.__props["additional_recipients"])
        self.__smtpObj.sendmail(self.__props["from"], tos_addr, self.__build_msg(tos_addr, content))
        #self.__smtpObj.quit()

    def send_to_admin(self, content):
        self.__smtpObj.login(self.__props["username"], self.__props["password"])
        tos_addr = []
        tos_addr.extend(self.__props["additional_recipients"])
        self.__smtpObj.sendmail(self.__props["from"], tos_addr, self.__build_msg(tos_addr, content))

    def __build_msg(self, to, content):
        msg = multipart.MIMEMultipart()
        msg["FROM"] = self.__props["from"]
        msg["TO"] = ",".join(to)
        msg["Subject"] = self.__props["subject"]

        body = self.__props["failure_message"]
        body += "\n\n" + content

        msg.attach(mimetext.MIMEText(body, "plain"))

        return msg.as_string()


if __name__ == "__main__":
    props = SdeArchivistProperties.SdeArchivistProperties("config/archivist_config.json").mail_config
    m = MailSender(props)
    m.send_to_admin("ADMIN TEST")