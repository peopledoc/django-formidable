# -*- coding: utf-8 -*-


class singleton(object):

    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
