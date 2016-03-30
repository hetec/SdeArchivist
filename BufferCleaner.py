import os


class BufferCleaner:

    def __init__(self):
        pass

    def set_console_logger(self, console_logger):
            self.__c_logger = console_logger

    def set_file_logger(self, file_logger):
        self.__f_logger = file_logger

    def clear_all(self, dir):
        #print "remove all"
        for d in os.walk(os.path.join(os.getcwd(), dir), topdown=False, ):

            #print d
            for f in d[2]:
                p = os.path.join(d[0],f)
                os.remove(p)
                self.__c_logger.debug("REMOVE from buffer: " + str(p))
                self.__f_logger.debug("REMOVE from buffer: " + str(p))
            os.rmdir(d[0])
        os.mkdir(dir)

    def clear_file(self, file_name):
        #print "remove file: " + file_name
        if os.access(os.path.join("buffer", file_name), os.F_OK):
            os.remove(os.path.join("buffer", file_name))
            self.__c_logger.debug("REMOVE from buffer: " + str(file_name))
            self.__f_logger.debug("REMOVE from buffer: " + str(file_name))
        else:
            pass
            #print "no file"

if __name__ == "__main__":
    BufferCleaner().clear_file("SDE.alles.xml")