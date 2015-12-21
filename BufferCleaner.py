import os


class BufferCleaner:

    def __init__(self):
        pass

    def clear_all(self, dir):
        print "remove all"
        for d in os.walk(os.path.join(os.getcwd(), dir), topdown=False, ):
            print d
            for f in d[2]:
                p = os.path.join(d[0],f)
                os.remove(p)
            os.rmdir(d[0])
        os.mkdir(dir)

    def clear_file(self, file_name):
        print "remove file: " + file_name
        if os.access(os.path.join("buffer", file_name), os.F_OK):

            os.remove(os.path.join("buffer", file_name))
        else:
            print "no file"

if __name__ == "__main__":
    BufferCleaner().clear_file("SDE.alles.xml")