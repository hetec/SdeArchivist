# -*- encoding utf-8 -*-
import smtplib
from email import MIMEText as mimetext
from email import MIMEMultipart as multipart


class MailSender:
    """
    Enables sending emails to a user or defined admins
    """

    def __init__(self, properties):
        """
        Creates a pre-configured instance

        :param properties: The mail configuration data (Map)
        """
        self.__props = properties
        #only ascii for the server and port
        self.__smtpObj = smtplib.SMTP(str(self.__props["smtp_server"]), str(self.__props["port"]))
        self.__smtpObj.starttls()


    def set_console_logger(self, console_logger):
        """
        Set a console logger

        :param console_logger: A logger instance
        """
        self.__c_logger = console_logger

    def set_file_logger(self, file_logger):
        """
        Set a file logger

        :param file_logger: A logger instance
        """
        self.__f_logger = file_logger

    def send(self, to, content, msg_type):
        """
        Send a email to a defined recipient. If 'get_user_process_info'
        is enabled in the config file the email is also send to the configured
        list of admins

        :param to: recipient (String)
        :param content: The message which is displayed after the default message configured in the config file (String)
        :param msg_type: Success or failure (String)
        """
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
            if self.__props["get_user_process_info"] == True:
                tos_addr.extend(self.__props["admin_recipients"])
            self.__smtpObj.sendmail(self.__props["from"], tos_addr, self.__build_msg(tos_addr, content, msg_type))
            self.__c_logger.info("Send mail to " + str(tos_addr))
            self.__f_logger.info("Send mail to " + str(tos_addr))
        except Exception as e:
            self.__c_logger.exception("Unable to send emails with: " + str(self.__props["username"]) + ", " + str(self.__props["password"]))
            self.__f_logger.exception("Unable to send emails with: " + str(self.__props["username"]) + ", " + str(self.__props["password"]))

    def send_to_admin(self, content):
        """
        Sends an email to the configured list of admins

        :param content: The main message of the email. Displayed after a predefined default message. (String)
        """
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
            tos_addr.extend(self.__props["admin_recipients"])
            self.__smtpObj.sendmail(self.__props["from"], tos_addr, self.__build_msg(tos_addr, content, "admin"))
            self.__c_logger.info("Send mail to " + str(tos_addr))
            self.__f_logger.info("Send mail to " + str(tos_addr))
        except Exception as e:
            self.__c_logger.exception("Unable to send admin emails.")
            self.__f_logger.exception("Unable to send admin emails.")

    def __build_msg(self, to, content, msg_type):
        """
        Constructs a message body from a given content and a configured default message.
        Sets also the SUBJECT and the FROM fields.

        :param to: recipient (String)
        :param content: The main message (String)
        :param msg_type: Success or Failure (String)
        :return: The message as string (String)
        """
        msg = multipart.MIMEMultipart()
        msg["FROM"] = self.__props["from"]
        msg["TO"] = ",".join(to)
        if msg_type == "failure":
            msg["Subject"] = self.__props["failure_subject"]
            body = self.__props["default_message"]
        elif msg_type == "success":
            msg["Subject"] = self.__props["success_subject"]
            body = self.__props["default_message"]
        elif msg_type == "admin":
            msg["Subject"] = "!!!ADMIN INFO: sde archiving"
            body = "The sde archiving service has behaved unexpected! Please see the message below:"
        else:
            raise ValueError(msg_type + " is not allowed. Please use failure or success")


        body += "\n\n" + content
        self.__c_logger.debug("Mail message: \n\n" +
                              msg.as_string())
        self.__f_logger.debug("Mail message: \n\n" +
                              msg.as_string())
        msg.attach(mimetext.MIMEText(body, "plain"))

        return msg.as_string()
