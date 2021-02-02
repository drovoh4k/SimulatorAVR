#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from avrexcep import OutOfMemError, UnknownCodeError, BreakException
from state import State
from instruction import Add, Adc, Sub, Subi, And, Or, Eor, Lsr, Mov, Ldi, Sts, Lds, Rjmp, Brbs, Brbc, Nop, Break, In, Out
from repertoir import Repertoir

class AvrMcu(object):
    """
    Executes the writed code of asambler of AVR.

    :param _s: State of simulator
    :type _rep: Instance of State
    :param _rep: Repertoir of instructions of the simulator
    :type _rep: Instance of Repertoir
    """
    def __init__(self):
        self._s = State()

        # Instance declaration of all instructions
        add = Add()
        adc = Adc()
        sub = Sub()
        subi = Subi()
        my_and = And()
        my_or = Or()
        eor = Eor()
        lsr = Lsr()
        mov = Mov()
        ldi = Ldi()
        sts = Sts()
        lds = Lds()
        rjmp = Rjmp()
        brbs = Brbs()
        brbc = Brbc()
        nop = Nop()
        brk = Break()
        my_in = In()
        my_out = Out()
        
        # Adding all instance to a list
        lst_instr = [add, adc, sub, subi, my_and, my_or, eor, lsr,
                    mov, ldi, sts, lds, rjmp, brbs, brbc, nop, brk, 
                    my_in, my_out]

        # Sending list to Repertoir
        self._rep = Repertoir(lst_instr)

        self.reset()

    def reset(self):
        """
        Reset the state.
        """
        self._s = State()
    
    def set_prog(self, p):
        """
        Installs a program on the memory.

        :param p: Program to install
        :type p: str of int
        """
        for x in range(len(p)):
            self._s.prog[x] = p[x]

    def dump_reg(self):
        """
        Return an string with the registers of the simulator.

        :return: Representation
        :rtype: str
        """
        return self._s.dump_reg()

    def dump_dat(self):
        """
        Return an string with the data memory of the simulator.

        :return: Representation
        :rtype: str
        """
        return self._s.dump_data()

    def dump_prog(self):
        """
        Return an string with the program memory of the simulator.

        :return: Representation
        :rtype: str
        """
        return self._s.dump_prog()

    def run(self):
        """
        Is the principal method of the simulator. When it's called it
        starts an infinite loop:

        (1) Obtain the instruction indicicated by PC
        (2) Find an InstRunner that can run the instruction
        (3) Executes the instruction

        Also has a catcher for diferent type of exceotions, such as
        OutOfMemError, UnknownCodeError and BreakException.
        """
        try:
            while True:
                # Get next instruction
                instruction = self._s.prog[self._s.pc]

                # Find InstRunner
                instrunner = self._rep.find(instruction)

                # Execute Instruction
                instrunner.execute(instruction, self._s)
        
        except OutOfMemError:
            print "Out of Memory"
            sys.exit()
            
        except UnknownCodeError:
            print "Unknown Code Error"
            sys.exit()
        
        except BreakException:
            sys.exit()


    def set_trace(self, t):
        """
        If t=True activates mode trace of data memory, else if t=False,
        deacrivate the mode.

        :param t: Active or deactive
        :type t: boolean
        """           
        if t:
            return self._s.data.trace_on()
        else:
            return self._s.data.trace_off()
        
            
