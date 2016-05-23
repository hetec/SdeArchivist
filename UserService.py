import cx_Oracle
from DataException import DataException



class UserService:
    """
    Service to create user accounts
    """

    def __init__(self, connection):
        """
        Creates a new UserService instance

        :param connection: A connection object (cx_Oracle connection object)
        :return: New UserService
        """
        self.con = connection

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

    def create_user(self, username, password):
            """
            Checks if an USER for the given username exists in the DB. If one exists, no
            new USER is create else the program adds a USER to DB named like the username part
            of the data set. After the user was added, he is granted the CONNECT role

            :param username The name of the user
            :param password The password for the user

            """

            try:
                cur = self.con.cursor()
                cur.execute("Select * from ALL_USERS Where ALL_USERS.USERNAME = '" + str(username.upper()) + "'")
                result = cur.fetchall()
                if len(result) <= 0:
                    self.__c_logger.info("User doesn't exist --> CREATE USER: " + str(username))
                    self.__f_logger.info("User doesn't exist --> CREATE USER: " + str(username))
                    cur.execute('CREATE USER ' + str(username) + ' IDENTIFIED BY ' + str(password) + ' DEFAULT TABLESPACE USERS')
                    self.__c_logger.info("Grant connect to user")
                    self.__f_logger.info("Grant connect to user")
                    cur.execute("GRANT CONNECT TO " + str(username.upper()))
                    self.con.commit()
                else:
                    self.__c_logger.info("User exists --> DONT CREATE USER: " + str(username))
                    self.__f_logger.info("User exists --> DONT CREATE USER: " + str(username))

            except cx_Oracle.DatabaseError as e:
                self.con.rollback()
                self.__c_logger.exception("EXCEPTION while creating user " + str(username) + ": " + str(e))
                self.__f_logger.exception("EXCEPTION while creating user " + str(username) + ": " + str(e))
                raise DataException("EXCEPTION while creating user " + str(username) + ": " + str(e))
            finally:
                cur.close()