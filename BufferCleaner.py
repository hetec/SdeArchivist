import os


class BufferCleaner:
    """
    Utility class to clean the buffer directory after the program is finished
    """

    def __init__(self):
        pass

    def set_console_logger(self, console_logger):
        """
        Set a console logger

        :param console_logger: logger instance
        """
        self.__c_logger = console_logger

    def set_file_logger(self, file_logger):
        """
        Set a file logger

        :param file_logger: logger instance
        """
        self.__f_logger = file_logger

    def clear_all(self, dir):
        """
        Clears all files in the dir directory

        :param dir: directory relative to the project root (String)
        """
        for d in os.walk(os.path.join(os.getcwd(), dir), topdown=False, ):
            for f in d[2]:
                p = os.path.join(d[0],f)
                os.remove(p)
                self.__c_logger.debug("REMOVE from buffer: " + str(p))
                self.__f_logger.debug("REMOVE from buffer: " + str(p))
            os.rmdir(d[0])
        os.mkdir(dir)

    def clear_file(self, file_name):
        """
        Removes the given file from the buffer directory

        :param file_name: The name of the file (String)
        """
        if os.access(os.path.join("buffer", file_name), os.F_OK):
            os.remove(os.path.join("buffer", file_name))
            self.__c_logger.debug("REMOVE from buffer: " + str(file_name))
            self.__f_logger.debug("REMOVE from buffer: " + str(file_name))
