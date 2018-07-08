# -*- coding: utf-8 -*-

""" Exceptions for module """


class SerialNumberMismatchException(Exception):
    """
    Thrown when a user enters a SN that does not match former SNs.
    """
    pass


class InvalidSerialNumberException(Exception):
    """
    Thrown when a SN does not conform to constraints proposed in serial_numbers.py.
    """
    pass
