# -*- encoding utf-8 -*-


class ExistenceException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)