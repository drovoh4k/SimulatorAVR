#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bitvec import Byte, Word
from memory import DataMemory, ProgramMemory

C, Z, N = 0, 1, 2 # CARRY, ZERO, NEG
class State(object):
    """
    Represents the state of MCU. Is formed by all the registers and
    memories. Every time an instruction is called, uses to change.

    :ivar data: Memory bank of data
    :vartype data: obj
    :ivar prog: Memory bank of program
    :vartype prog: obj
    :ivar pc: Program Counter
    :vartype pc:
    :ivar flags: Register status
    :vartype flags: int
    """
    def __init__(self, data=128, prog=128):
        self.data = DataMemory(data)
        self.prog = ProgramMemory(prog)
        self.pc = Word()
        self.flags = Byte()

    def dump_data(self):
        """
        Represents the content of data memory.

        :return: Representation
        :rtype: str
        """
        return str(self.data.dump(32, 128))

    def dump_prog(self): # Missing
        """
        Represents the content of progam memeory.

        :return: Representation
        :rtype: str
        """
        return str(self.prog.dump(0, 128))

    def dump_reg(self):
        """
        Represents the registers of the state like this:

        R00: 00
        R01: 00
        ...
        R31: 00
        X(R27:R26): 0000
        Y(R29:R28): 0000
        Z(R31:R30): 0000
        PC: 0000
        CARRY: 0 ZERO: 0 NEG: 0

        :return: Representation
        :rtype: str
        """
        reg_1 = self.data.dump_reg()

        pc = str(self.pc)
        reg_2 = "PC: {0}".format(pc)
        
        flag_1 = int(self.flags[C] == True)
        flag_2 = int(self.flags[Z] == True)
        flag_3 = int(self.flags[N] == True)
        reg_3 = "CARRY: {0} ZERO: {1} NEG: {2}".format(flag_1, flag_2, flag_3)

        return "{0}\n{1}\n{2}".format(reg_1, reg_2, reg_3)
