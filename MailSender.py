# -*- encoding utf-8 -*-
import smtplib
from email import MIMEText as mimetext
from email import MIMEMultipart as multipart


class MailSender:
    """
    Enables sending emails to a assigned user
    """

    def __init__(self, properties):
        self.__props = properties
        #only ascii for the server and port
        self.__smtpObj = smtplib.SMTP(str(self.__props["smtp_server"]), str(self.__props["port"]))
        self.__smtpObj.starttls()


    def set_console_logger(self, console_logger):
        self.__c_logger = console_logger

    def set_file_logger(self, file_logger):
        self.__f_logger = file_logger

    def send(self, to, content):
        try:
            self.__c_logger.debug("Mail connection: " +
                              str(self.__props["smtp_server"]) + ", " +
                              str(self.__props["port"]))
            self.__f_logger.debug("Mail connection: " +
                                  str(self.__props["smtp_server"]) + ", " +
                                  str(self.__props["port"]))
            self.__smtpObj.login(self.__props["username"], self.__props["password"])
            self.__c_logger.info("Log in to email server.")
            self.__f_logger.info("Log in to email server.")
            tos_addr = [to]
            tos_addr.extend(self.__props["additional_recipients"])
            self.__smtpObj.sendmail(self.__props["from"], tos_addr, self.__build_msg(tos_addr, content))
            self.__c_logger.info("Send mail to " + str(tos_addr))
            self.__f_logger.info("Send mail to " + str(tos_addr))
        except Exception as e:
            self.__c_logger.exception("Unable to send emails.")
            self.__f_logger.exception("Unable to send emails.")

    def send_to_admin(self, content):
        try:
            self.__c_logger.debug("Mail connection: " +
                              str(self.__props["smtp_server"]) + ", " +
                              str(self.__props["port"]))
            self.__f_logger.debug("Mail connection: " +
                                  str(self.__props["smtp_server"]) + ", " +
                                  str(self.__props["port"]))
            self.__smtpObj.login(self.__props["username"], self.__props["password"])
            self.__c_logger.info("Log in to email server.")
            self.__f_logger.info("Log in to email server.")
            tos_addr = []
            tos_addr.extend(self.__props["additional_recipients"])
            self.__smtpObj.sendmail(self.__props["from"], tos_addr, self.__build_msg(tos_addr, content))
            self.__c_logger.info("Send mail to " + str(tos_addr))
            self.__f_logger.info("Send mail to " + str(tos_addr))
        except Exception as e:
            self.__c_logger.exception("Unable to send admin emails.")
            self.__f_logger.exception("Unable to send admin emails.")

    def __build_msg(self, to, content):
        msg = multipart.MIMEMultipart()
        msg["FROM"] = self.__props["from"]
        msg["TO"] = ",".join(to)
        msg["Subject"] = self.__props["subject"]

        body = self.__props["failure_message"]
        body += "\n\n" + content
        self.__c_logger.debug("Mail message: \n\n" +
                              msg.as_string())
        self.__f_logger.debug("Mail message: \n\n" +
                              msg.as_string())
        msg.attach(mimetext.MIMEText(body, "plain"))

        return msg.as_string()


if __name__ == "__main__":

    pass