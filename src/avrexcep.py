#!/usr/bin/env python
# -*- coding: utf-8 -*-

class AVRException(Exception):
    """ Base class for other exceptions """
    pass


class OutOfMemError(AVRException):
    """ Raised when denotes an acces to an inexistent adress """
    pass


class BreakException(AVRException):
    """ Raised when instruction BRK is executed """
    pass


class UnknownCodeError(AVRException):
    """ Raises when given instruction is unknown """
    pass
