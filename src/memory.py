#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bitvec import Byte, Word
from avrexcep import OutOfMemError

from bitvec import Word, Byte

class Memory(object):
    """
    Represents a memory bank. 

    :ivar _m: Bank of memory
    :vartype _m: list
    :ivar _trace: Trace activated or deactivated
    :vartype _trace: bool

    """
    def __init__(self):
        self._m = [] # In subclasses will be an object of Word or Byte
        self._trace = False

    def trace_on(self):
        """
        Activates the trace
        """
        self._trace = True

    def trace_off(self):
        """
        Deactivates the trace
        """
        self._trace = False

    def __len__(self):
        return len(self._m)

    def __repr__(self):
        if len(self._m[0]) == 8: # Byte
            result = ""
            for x in range(len(self._m)):
                hex_dir = hex(x).zfill(4).upper() # Memory direction
                hex_con = str(self._m[x]).zfill(2).upper() # Memory content
                result = result + "{0}: {1}\n".format(hex_dir, hex_con)
            return result
        else: # Word
            result = ""
            for x in range(len(self._m)):
                hex_dir = hex(x).zfill(4).upper() # Memory direction
                hex_con = str(self._m[x]).zfill(4).upper() # Memory content
                result = result + "{0}: {1}\n".format(hex_dir, hex_con)
            return result
        
    def dump(self, f=0, t=5):
        """
        Check stored data of an interval.

        :param f: Left of interval
        :tyoe f: int
        :param t; Right of an interval
        :type t: int

        :return: Stored data
        :rtype: str
        """
        if len(self._m[0]) == 8: # Byte
            result = ""
            for x in range(f,t):
                hex_dir = hex(x).zfill(4).upper() # Memory direction
                hex_con = str(self._m[x]).zfill(4).upper() # Memory content
                result = result + "{0}: {1}\n".format(hex_dir, hex_con)
            return result
        else: # Word
            result = ""
            for x in range(f,t):
                hex_dir = hex(x).zfill(4).upper() # Memory direction
                hex_con = str(self._m[x]).zfill(4).upper() # Memory content
                result = result + "{0}: {1}\n".format(hex_dir, hex_con)
            return result
            
    def __getitem__(self, addr):
        addr = int(addr)
        if addr < len(self._m):
            if self._trace:
                hex_dir = hex(addr).zfill(4).upper() # Memory direction
                hex_con = self._m[addr] # Memory content
                print "Read {0} from {1}".format(hex_con, hex_dir)
            return self._m[addr]
        else:
            hex_dir = hex(addr).zfill(4).upper() # Memory direction
            print "Read from {0} out of range".format(hex_dir)
            error = OutOfMemError()
        
    def __setitem__(self, addr, val):
        addr = int(addr)
        if addr < len(self._m):
            if self._trace:
                hex_dir = hex(addr).zfill(4).upper() # Memory direction
                hex_con = str(val) # Memory content
                print "Write {0} to {1}".format(hex_con, hex_dir)
                
            if type(val) is int: # Cheks if val is a int
                my_word = Word(val)
                self._m[addr] = my_word
            else:
                self._m[addr] = val
        else:
             hex_dir = hex(addr).zfill(4).upper() # Memory direction
             print "Write to {0} out of range".format(hex_dir)
             error = OutOfMemError()

class ProgramMemory(Memory):
    """
    Represents a bank of memory for store data. The stored data are
    Bytes.

    :param ncells: Number of cells
    :type ncells: int
    """
    def __init__(self, ncells=1024):
        self._trace = False
        
        memory_bank = []
        for x in range(ncells):
            my_word = Word()
            memory_bank.append(my_word)
        self._m = memory_bank


class DataMemory(Memory):
    """
    Represents a bank of memory for store programs. The stored data
    are Words.

    :param ncells: Number of cells
    :type ncells: int
    """  
    def __init__(self, ncells=1024):
        self._trace = False
        
        ncell = ncells if ncells>32 else 32
        memory_bank = []
        for x in range(ncells):
            my_byte = Byte()
            memory_bank.append(my_byte)
        self._m = memory_bank

    def dump_reg(self):
        """
        Represents the registers stored in a bank of memory in a
        format like this:

        R00: 00
        R01: 00
        ...
        R31: 00
        X(R27:R26): 0000
        Y(R29:R28): 0000
        Z(R31:R30): 0000

        :return: Registers
        :rtype: str
        """
        register = ""
        for x in range(32): # Adding registers from 00 to 31
            reg_num = str(x).zfill(2)
            hex_con = str(self._m[x]).zfill(2).upper() # Memory content
            register = register + "R{0}: {1}\n".format(reg_num, hex_con)

        reg_x = self._m[27] + self._m[26]
        register = register + "X(R27:R26): {0}\n".format(str(reg_x).zfill(4)) # Adding X
        reg_y = self._m[29] + self._m[28]
        register = register + "Y(R29:R28): {0}\n".format(str(reg_y).zfill(4)) # Adding Y
        reg_z = self._m[31] + self._m[30]
        register = register + "Z(R31:R30): {0}".format(str(reg_z).zfill(4)) # Adding Z

        return register


if __name__ == '__main__':
    word = Word(456)
    memory = DataMemory()
    memory._m[300] = word
    memory._m[301] = word
    memory._m[304] = word
    memory._m[307] = word

    #print memory
    
    print memory.dump_reg()
