import cx_Oracle
import random
import string

from DataException import DataException


class UserService:
    """
    Service to create user accounts
    """

    def __init__(self, db_connection, archive_connection, mail_provider):
        """
        Creates a new UserService instance

        :param db_connection: A connection object to connect to the original arcSde db (cx_Oracle connection object)
        :param archive_connection: A connection object to connect to the archive arcSde db (cx_Oracle connection object)
        :param mail_provider: A MailSender instance to send error messages
        :return: New UserService
        """
        self.archive_con = archive_connection
        self.db_con = db_connection
        self.mail = mail_provider

    def set_console_logger(self, console_logger):
        """
        Set the console logger

        :param console_logger: logger instance
        """
        self.__c_logger = console_logger

    def set_file_logger(self, file_logger):
        """
        Set the file logger

        :param file_logger: logger instance
        """
        self.__f_logger = file_logger

    def create_user(self, username):
            """
            Checks if an USER for the given username exists in the DB. If one exists, no
            new USER is create else the program adds a USER to DB named like the username part
            of the data set. After the user was added, he is granted the CONNECT role

            :param username: The name of the user
            :exception DataException
            """

            cur = None
            try:
                cur = self.archive_con.cursor()
                user_exists = self.__user_exists(str(username), self.archive_con)
                if not user_exists:
                    pw_hash = self.__fetch_original_password_hash(str(username))
                    if pw_hash:
                        self.__c_logger.info("Create user from hash: " + str(username))
                        self.__f_logger.info("Create user from hash: " + str(username))
                        cur.execute("CREATE USER " + str(username) + " IDENTIFIED BY VALUES '" +
                                    str(pw_hash) + "' DEFAULT TABLESPACE USERS")
                        self.__grant_connect_to_user(str(username))
                    else:
                        self.__c_logger.info("No hash, create user with default pw (username): " + str(username))
                        self.__f_logger.info("No hash, create user with default pw (username): " + str(username))
                        # Create a 8 digests long random string
                        random_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
                        random_key = 'PW' + random_key
                        cur.execute("CREATE USER " + str(username) + " IDENTIFIED BY " + random_key +
                                    " DEFAULT TABLESPACE USERS")
                        self.__grant_connect_to_user(str(username))
                        #  Send mail to admin
                        self.mail.send_to_admin("USER: " + str(username) + " was created with a random password! " +
                                                "Please CHANGE the password and inform the concerned user")
                    self.archive_con.commit()
                else:
                    self.__c_logger.info("Don't create user: " + str(username))
                    self.__f_logger.info("Don't create user: " + str(username))

            except Exception as e:
                self.__c_logger.exception("EXCEPTION while creating user " + str(username) + ": " + str(e))
                self.__f_logger.exception("EXCEPTION while creating user " + str(username) + ": " + str(e))
                raise DataException("EXCEPTION while creating user " + str(username) + ": " + str(e))
            finally:
                if cur is not None:
                    cur.close()

    def __fetch_original_password_hash(self, username):
            cur = None
            try:
                self.__c_logger.info("Get pw hash for user: " + str(username))
                self.__f_logger.info("Get pw hash for user: " + str(username))
                cur = self.db_con.cursor()
                # Get the pw hash for the given username from the original arcSde db
                cur.execute("SELECT spare4 FROM sys.USER$ WHERE sys.USER$.NAME = '" + str(username.upper()) + "'")
                result = cur.fetchall()
                if len(result) > 0:
                    hash = str(result[0][0])
                    self.__c_logger.info("User exists, password hash: " + str(hash))
                    self.__f_logger.info("User doesn't exist --> CREATE USER: " + str(hash))
                    # return the pw hash if it exists
                    return str(hash)
                else:
                    self.__c_logger.info("User not found: Use username as default password")
                    self.__f_logger.info("User not found: Use username as default password")
                    # return an empty string if the hash doesn't exist
                    return ""

            except Exception as e:
                self.__c_logger.exception("EXCEPTION while fetching pw hash for user " + str(username) + ": " + str(e))
                self.__f_logger.exception("EXCEPTION while fetching pw hash for user " + str(username) + ": " + str(e))
                return ""
            finally:
                if cur is not None:
                    cur.close()

    def __grant_connect_to_user(self, username):
            cur = None
            try:
                cur = self.archive_con.cursor()
                # Get the pw hash for the given username from the original arcSde db
                user_exists = self.__user_exists(str(username), self.archive_con)
                if user_exists:
                    self.__c_logger.info("User exists in archive: " + str(username))
                    self.__f_logger.info("User exists in archive: " + str(username))
                    self.__c_logger.info("Grant connect to user")
                    self.__f_logger.info("Grant connect to user")
                    cur.execute("GRANT CONNECT TO " + str(username.upper()))
                else:
                    self.__c_logger.info("User not found: Cannot grant connect to user")
                    self.__f_logger.info("User not found: Cannot grant connect to user")
                    raise DataException("No user found to grant CONNECT role:  " + str(username))

            except Exception as e:
                self.__c_logger.exception("EXCEPTION while granting connect to user " + str(username) + ": " + str(e))
                self.__f_logger.exception("EXCEPTION while granting connect to user " + str(username) + ": " + str(e))
                raise DataException("EXCEPTION while granting connect to user " + str(username) + ": " + str(e))
            finally:
                if cur is not None:
                    cur.close()

    def __user_exists(self, username, connection):
            cur = None
            try:
                cur = connection.cursor()
                cur.execute("Select * from ALL_USERS Where ALL_USERS.USERNAME = '" + str(username.upper()) + "'")
                result = cur.fetchall()
                if len(result) <= 0:
                    self.__c_logger.info("User doesn't exist" + str(username))
                    self.__f_logger.info("User doesn't exist" + str(username))
                    return False
                else:
                    self.__c_logger.info("User exists: " + str(username))
                    self.__f_logger.info("User exists: " + str(username))
                    return True

            except Exception as e:
                self.__c_logger.exception("EXCEPTION while checking existence of user " + str(username) + ": " + str(e))
                self.__f_logger.exception("EXCEPTION while checking existence of user " + str(username) + ": " + str(e))
                raise DataException("EXCEPTION while checking existence of user " + str(username) + ": " + str(e))
            finally:
                if cur is not None:
                    cur.close()