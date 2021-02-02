#!/usr/bin/env python
# -*- coding: utf-8 -*-

from avrexcep import UnknownCodeError

class Repertoir(object):
    """
    Represents a set of instructions of an MCU. If we give an
    instruction it returns the corresponding InstRunner object.

    :param li: List of instances of InstRunner
    :type li: list of objects
    """
    def __init__(self, li):
        self._li = li

    def find(self, instr):
        """
        Find an instance of InstRunner that can execute intruction
        instr. If it exists it return it, else UnknownCodeError
        raises.

        :param instr: Intruction
        :type instr: instance from Word

        :return: Intruction
        :rtype: instance of InstRunner
        """
        for x in self._li:
            if x.match(instr):
                return x
        else:
            raise UnknownCodeError
