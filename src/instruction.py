#!/usr/bin/env python
# -*- coding: utf-8 -*-

from avrexcep import OutOfMemError, BreakException
from bitvec import Byte, Word

from state import State

C, Z, N = 0, 1, 2 # CARRY, ZERO, NEG

class InstRunner(object):
    """
    This class is abstract, is the superclass of all the instructions
    and contains the common methods between all of them.
    """
    def __repr__(self):
        return self.name

    def match(self, instr):
        """
        Checks if this instance can execute a certain instruction

        :param instr: Instruction to be checked
        :type instr: object from Word

        :return: True if can be executed // False if can not
        :rtype: boolean
        """
        instr = instr.extract_field_u(self._mask)

        return instr == self._code

    def execute(self, instr, state):
        """
        Executes an instruction and as a result, modifies the state of
        the microcontroller which is accessing to. The steps are: 
        (1) Decode the instruction - Apply mask
        (2) Obtanin the opearators (feth)
        (3) Calculate the result
        (4) Modify the register of state
        (4) Store the result

        :param instr: Instruction to be executed
        :type instr: object from Word
        :param state: State to modify
        :type state: object from State
        """
        pass


class Add(InstRunner):
    """
    Add without Carry - Adds two registers without the C Flag and
    places the result in the destination register Rd.

    Operation:
    Rd <= Rd + Rr

    Syntax:                Operands:                Program Counter:         
    ADD Rd,Rr              0=<d=<31, 0=<r=<31       PC <= PC + 1

    16-bit Opcode:
    0000 11rd dddd rrrr 

    *N -> R7 
          (Set if MSB of the result is set; cleared otherwise.)
    *Z -> ~R7 * ~R6 * ~R5 * ~R4 * ~R3 * ~R2 * ~R1 * ~R0
          (Set if the result is $00; cleared otherwise.)
    *C -> Rd7 * Rr7 + Rr7 * ~R7 + ~R7 * Rd7
          (Set if the absolute value of the contents of Rr is larger
          than the absolute value of Rd; cleared
          otherwise.)
    R (Result) equals Rd after the operation.
    """
    def __init__(self):
        self.name = "Add"
        self._mask = "1111110000000000"
        self._code = "0b0000110000000000"

    def execute(self, instr, state):
        # Convert instr to bin
        instr = bin(instr).replace("0b", "").zfill(16)

        # Extract register R
        reg_r = str(int(instr[6]))
        for x in range(12,16):
            reg_r = reg_r + str(int(instr[x]))
        reg_r = int(reg_r, 2) # Convert to int

        # Extract register G
        reg_d = ""
        for x in range(7,12):
            reg_d = reg_d + str(int(instr[x]))
        reg_d = int(reg_d, 2) # Convert to int
        
        # Extract content of registers
        vector_r = state.data[reg_r]
        vector_d = state.data[reg_d]

        # Operate with contents of registers
        result = vector_r + vector_d

        # Extract the carry
        if int(result) > 255:
            result = result - 255
            # Flag CARRY
            state.flags[C] = 1
        else:
            state.flags[C] = 0

        # Assign the result to the register
        state.data[reg_r] = result

        # Increments PC by 1
        state.pc = state.pc + 1
        
        # Flag NEG
        state.flags[N] = int(bin(result)[0] == '-')
        
        # Flag ZERO
        state.flags[Z] = int(int(result) == 0)


class Adc(InstRunner):
    """
    Add with Carry - Adds two registers and the contents of the C Flag
    and places the result in the destination register.

    Operation:
    Rd <= Rd + Rr

    Syntax:                Operands:                Program Counter:         
    ADD Rd,Rr              0=<d=<31, 0=<r=<31       PC <= PC + 1

    16-bit Opcode:
    0001 11rd dddd rrrr

    *N -> R7 
          (Set if MSB of the result is set; cleared otherwise.)
    *Z -> ~R7 * ~R6 * ~R5 * ~R4 * ~R3 * ~R2 * ~R1 * ~R0
          (Set if the result is $00; cleared otherwise.)
    *C -> Rd7 * Rr7 + Rr7 * ~R7 + ~R7 * Rd7
          (Set if the absolute value of the contents of Rr is larger
          than the absolute value of Rd; cleared
          otherwise.)
    R (Result) equals Rd after the operation.
    """
    def __init__(self):
        self.name = "Adc"
        self._mask = "1111110000000000"
        self._code = "0b0001110000000000"

    def execute(self, instr, state):
        # Convert instr to bin
        instr = bin(instr).replace("0b", "").zfill(16)

        # Extract register R
        reg_r = str(int(instr[6]))
        for x in range(12,16):
            reg_r = reg_r + str(int(instr[x]))
        reg_r = int(reg_r, 2) # Convert to int

        # Extract register G
        reg_d = ""
        for x in range(7,12):
            reg_d = reg_d + str(int(instr[x]))
        reg_d = int(reg_d, 2) # Convert to int
        
        # Extract content of registers
        vector_r = state.data[reg_r]
        vector_d = state.data[reg_d]

        # Operate with contents of registers
        result = vector_r + vector_d + int(state.flags[C])

        # Extract the carry
        if int(result) > 255:
            result = result - 255
            # Flag CARRY
            state.flags[C] = 1
        else:
            state.flags[C] = 0

        # Assign the result to the register
        state.data[reg_r] = result

        # Increments PC by 1
        state.pc = state.pc + 1
        
        # Flag NEG
        state.flags[N] = int(bin(result)[0] == '-')
        
        # Flag ZERO
        state.flags[Z] = int(int(result) == 0)


class Sub(InstRunner):
    """
    Substract without Carry - ubtracts two registers and places the
    result in the destination register Rd.

    Operation:
    Rd <= Rd - Rr 

    Syntax:                Operands:                Program Counter:         
    SUB Rd,Rr              0=<d=<31, 0=<r=< 255     PC <= PC + 1

    16-bit Opcode:
    0001 10rd dddd rrrr

    Status register:
    N  Z  C
    *  *  *

    *N -> R7 
          (Set if MSB of the result is set; cleared otherwise.)
    *Z -> ~R7 * ~R6 * ~R5 * ~R4 * ~R3 * ~R2 * ~R1 * ~R0
          (Set if the result is $00; cleared otherwise.)
    *C -> ~Rd7 * Rr7 + Rr7 * R7 + R7 * ~Rd7
          (Set if the absolute value of the contents of Rr is larger
          than the absolute value of Rd; cleared
          otherwise.)
    """
    def __init__(self):
        self.name = "Sub"
        self._mask = "1111110000000000"
        self._code = "0b0001100000000000"

    def execute(self, instr, state):
        # Convert instr to bin
        instr = bin(instr).replace("0b", "").zfill(16)

        # Extract register Rr
        reg_r = str(int(instr[6]))
        for x in range(12,16):
            reg_r = reg_r + str(int(instr[x]))
        reg_r = int(reg_r, 2) # Convert to int

        # Extract register Rd
        reg_d = ""
        for x in range(7,12):
            reg_d = reg_d + str(int(instr[x]))
        reg_d = int(reg_d, 2) # Convert to int

        # Extract content of registers
        vector_d = state.data[reg_d]
        vector_r = state.data[reg_r]
        
        # Operate with contents of registers
        result = vector_d - vector_r

        # Extract the carry
        if int(result) >= 255:
            result = result - 255
            # Flag CARRY
            state.flags[C] = 1
        else:
            state.flags[C] = 0

        # Assign the result to the register
        state.data[reg_d] = result

        # Increments PC by 1
        state.pc = state.pc + 1

        # Flag NEG
        state.flags[N] = int(bin(result)[0] == '-')
        
        # Flag ZERO
        state.flags[Z] = int(int(result) == 0)


class Subi(InstRunner):
    """
    Substract Immediate - Subtracts a register and a constant, and
    places the result in the destination register Rd. This instruction
    is working on Register R16 to R31 and is very well suited for
    operations on the X, Y, and Z-pointers.

 Operation:
    Rd <= Rd - K

    Syntax:                Operands:                Program Counter:         
    SUB Rd,K               0=<d=<31, 0=<K=< 255     PC <= PC + 1

    16-bit Opcode:
    0101 KKKK dddd KKKK

    Status register:
    N  Z  C
    *  *  *

    *N -> R7 
          (Set if MSB of the result is set; cleared otherwise.)
    *Z -> ~R7 * ~R6 * ~R5 * ~R4 * ~R3 * ~R2 * ~R1 * ~R0
          (Set if the result is $00; cleared otherwise.)
    *C -> ~Rd7 * Rr7 + Rr7 * R7 + R7 * ~Rd7
          (Set if the absolute value of the contents of Rr is larger
          than the absolute value of Rd; cleared
          otherwise.)
    """
    def __init__(self):
        self.name = "Add"
        self._mask = "1111000000000000"
        self._code = "0b0101000000000000"

    def execute(self, instr, state):
        # Convert instr to bin
        instr = bin(instr).replace("0b", "").zfill(16)

        # Extract constant
        K = ""
        for x in range(4,7):
            K = K + str(int(instr[x]))
        for x in range(12,16):
            K = K + str(int(instr[x]))
        K = int(K, 2) # Convert to int

        # Extract register Rd
        reg_d = ""
        for x in range(7,12):
            reg_d = reg_d + str(int(instr[x]))
        reg_d = int(reg_d, 2) + 16 # Convert to int

        # Extract content of register d
        vector_d = state.data[reg_d]
        
        # Operate with contents of registers
        result = vector_d - K

        # Extract the carry
        if int(result) >= 255:
            result = result - 255
            # Flag CARRY
            state.flags[C] = 1
        else:
            state.flags[C] = 0

        # Assign the result to the register
        state.data[reg_d] = result

        # Increments PC by 1
        state.pc = state.pc + 1

        # Flag NEG
        state.flags[N] = int(bin(result)[0] == '-')
        
        # Flag ZERO
        state.flags[Z] = int(int(result) == 0)


class And(InstRunner):
    """
    Logical AND - Performs the logical AND between the contents of
    register Rd and register Rr, and places the result in the
    destination register Rd.

    Operation:
    Rd <= Rd & Rr

    Syntax:                Operands:                Program Counter:         
    AND Rd,Rr              0=<d=<31, 0=<r=<31       PC <= PC + 1

    16-bit Opcode:
    0010 00rd dddd rrrr

    Status register:
    N  Z  C
    *  *  -

    *N -> R7 
          (Set if MSB of the result is set; cleared otherwise.)
    *Z -> ~R7 * ~R6 * ~R5 * ~R4 * ~R3 * ~R2 * ~R1 * ~R0
          (Set if the result is $00; cleared otherwise.)
    """
    def __init__(self):
        self.name = "And"
        self._mask = "1111110000000000"
        self._code = "0b0010000000000000"

    def execute(self, instr, state):
        # Convert instr to bin
        instr = bin(instr).replace("0b", "").zfill(16)

        # Extract register Rr
        reg_r = str(int(instr[6]))
        for x in range(12,16):
            reg_r = reg_r + str(int(instr[x]))
        reg_r = int(reg_r, 2) # Convert to int

        # Extract register Rd
        reg_d = ""
        for x in range(7,12):
            reg_d = reg_d + str(int(instr[x]))
        reg_d = int(reg_d, 2) # Convert to int

        # Extract content of registers
        vector_d = state.data[reg_d]
        vector_r = state.data[reg_r]

        # Operate with contents of registers
        result  = vector_d & vector_r

        # Assign the result to the register
        state.data[reg_d] = result

        # Increments PC by 1
        state.pc = state.pc + 1

        # Flag NEG
        state.flags[N] = int(bin(result)[0] == '-')
        
        # Flag ZERO
        state.flags[Z] = int(int(result) == 0)


class Or(InstRunner):
    """
    Performs the logical OR between the contents of register Rd and
    register Rr, and places the result in the destination register Rd.

    Operation:
    Rd <= Rd | Rr

    Syntax:                Operands:                Program Counter:         
    OR Rd,Rr              0=<d=<31, 0=<r=<31        PC <= PC + 1

    16-bit Opcode:
    0010 10rd dddd rrrr

    Status register:
    N  Z  C
    *  *  -

    *N -> R7 
          (Set if MSB of the result is set; cleared otherwise.)
    *Z -> ~R7 * ~R6 * ~R5 * ~R4 * ~R3 * ~R2 * ~R1 * ~R0
          (Set if the result is $00; cleared otherwise.)
    """
    def __init__(self):
        self.name = "Or"
        self._mask = "1111110000000000"
        self._code = "0b0010100000000000"

    def execute(self, instr, state):
        # Convert instr to bin
        instr = bin(instr).replace("0b", "").zfill(16)

        # Extract register Rr
        reg_r = str(int(instr[6]))
        for x in range(12,16):
            reg_r = reg_r + str(int(instr[x]))
        reg_r = int(reg_r, 2) # Convert to int

        # Extract register Rd
        reg_d = ""
        for x in range(7,12):
            reg_d = reg_d + str(int(instr[x]))
        reg_d = int(reg_d, 2) # Convert to int

        # Extract content of registers
        vector_d = state.data[reg_d]
        vector_r = state.data[reg_r]
        
        # Operate with contents of registers
        result = vector_d | vector_r

        # Assign the result to the register
        state.data[reg_d] = result

        # Increments PC by 1
        state.pc = state.pc + 1

        # Flag NEG
        state.flags[N] = int(bin(result)[0] == '-')
        
        # Flag ZERO
        state.flags[Z] = int(int(result) == 0)


class Eor(InstRunner):
    """
    Performs the logical EOR between the contents of register Rd and
    register Rr and places the result in the destination register Rd.

    Operation:
    Rd <= Rd ^ Rr

    Syntax:                Operands:                Program Counter:         
    EOR Rd,Rr              0=<d=<31, 0=<r=<31       PC <= PC + 1

    16-bit Opcode:
    0010 01rd dddd rrrr

    Status register:
    N  Z  C
    *  *  -

    *N -> R7 
          (Set if MSB of the result is set; cleared otherwise.)
    *Z -> ~R7 * ~R6 * ~R5 * ~R4 * ~R3 * ~R2 * ~R1 * ~R0
          (Set if the result is $00; cleared otherwise.)
    """
    def __init__(self):
        self.name = "Eor"
        self._mask = "1111110000000000"
        self._code = "0b0010010000000000"

    def execute(self, instr, state):
        # Convert instr to bin
        instr = bin(instr).replace("0b", "").zfill(16)

        # Extract register Rr
        reg_r = str(int(instr[6]))
        for x in range(12,16):
            reg_r = reg_r + str(int(instr[x]))
        reg_r = int(reg_r, 2) # Convert to int

        # Extract register Rd
        reg_d = ""
        for x in range(7,12):
            reg_d = reg_d + str(int(instr[x]))
        reg_d = int(reg_d, 2) # Convert to int

        # Extract content of registers
        vector_d = state.data[reg_d]
        vector_r = state.data[reg_r]
        
        # Operate with contents of registers
        result = vector_d ^ vector_r

        # Assign the result to the register
        state.data[reg_d] = result

        # Increments PC by 1
        state.pc = state.pc + 1

        # Flag NEG
        state.flags[N] = int(bin(result)[0] == '-')
        
        # Flag ZERO
        state.flags[Z] = int(int(result) == 0)


class Lsr(InstRunner):
    """
    Shifts all bits in Rd one place to the right. Bit 7 is
    cleared. Bit 0 is loaded into the C Flag of the SREG.This
    operation effectively divides an unsigned value by two. The C Flag
    can be used to round the result.

    Operation:
    

    Syntax:                Operands:                Program Counter:         
    LSR Rd                 0=<d=<31                 PC <= PC + 1

    16-bit Opcode:
    1001 010d dddd 0110

    Status register:
    N  Z  C
    0  *  *

    *Z -> R7 
          (Set if MSB of the result is set; cleared otherwise.)
    *C -> ~R7 * ~R6 * ~R5 * ~R4 * ~R3 * ~R2 * ~R1 * ~R0
          (Set if the result is $00; cleared otherwise.)
    """
    def __init__(self):
        self.name = "Lsr"
        self._mask = "1111111000001111"
        self._code = "0b1001010000000110"

    def execute(self, instr, state):
        # Convert instr to bin
        instr = bin(instr).replace("0b", "").zfill(16)

        # Extract reg_d
        reg_d = ""
        for x in range(7,12):
            reg_d = reg_d + str(int(instr[x]))
        reg_d = int(reg_d, 2) # Convert to int

        # Extract content of register d
        vector_d = state.data[reg_d]

        # Flag CARRY
        state.flags[C] = int(vector_d[0])

        # Operate with contents of registers
        result = vector_d >> 1
        result[7] = 0

        # Assign the result to the register
        state.data[reg_d] = result

        # Increments PC by 1
        state.pc = state.pc + 1

        # Flag NEG
        state.flags[N] = 0

        # Flag ZERO
        state.flags[Z] = int(int(result) == 0)


class Mov(InstRunner):
    """
    This instruction makes a copy of one register into another. The
    source register Rr is left unchanged, while the destination
    register Rd is loaded with a copy of Rr.

    Operation:
    Rd <= Rr

    Syntax:                Operands:                Program Counter:         
    MOV Rd,Rr              0=<d=<31, 0=<r=<31       PC <= PC + 1

    16-bit Opcode:
    0010 11rd dddd rrrr

    Status register:
    N  Z  C
    -  -  -
    """
    def __init__(self):
        self.name = "Mov"
        self._mask = "1111110000000000"
        self._code = "0b0010110000000000"

    def execute(self, instr, state):
        # Convert instr to bin
        instr = bin(instr).replace("0b", "").zfill(16)

        # Extract register Rr
        reg_r = str(int(instr[6]))
        for x in range(12,16):
            reg_r = reg_r + str(int(instr[x]))
        reg_r = int(reg_r, 2) # Convert to int

        # Extract register Rd
        reg_d = ""
        for x in range(7,12):
            reg_d = reg_d + str(int(instr[x]))
        reg_d = int(reg_d, 2) # Convert to int

        # Extract content of registers
        result = state.data[reg_r]

        # Assign the result to the register
        state.data[reg_d] = result

        # Increments PC by 1
        state.pc = state.pc + 1


class Ldi(InstRunner):
    """
    Loads an 8-bit constant directly to register 16 to 31.

    Operation:
    Rd <= k

    Syntax:                Operands:                Program Counter:         
    LDI Rd,k               16 =< 31, 0 =< 255       PC <= PC + 1

    16-bit Opcode:
    1110 KKKK dddd KKKK

    Status register:
    N  Z  C
    -  -  -
    """
    def __init__(self):
        self.name = "Ldi"
        self._mask = "1111000000000000"
        self._code = "0b1110000000000000"

    def execute(self, instr, state):
        # Convert instr to bin
        instr = bin(instr).replace("0b", "").zfill(16)

        # Extract register d
        reg_d = ""
        for x in range(8,12):
            reg_d = reg_d + str(int(instr[x]))
        reg_d = int(reg_d, 2) # Convert to int
        reg_d = reg_d + 16 # Start on 16

        # Extract value K
        value_k = ""
        for x in range(4,8):
            value_k = value_k + str(int(instr[x]))
        for x in range(12,16):
            value_k = value_k + str(int(instr[x]))
        value_k = int(value_k, 2) # Convert to int
        
        # Asign value k to register d        
        state.data[reg_d] = value_k
        
        # Increments PC by 1
        state.pc = state.pc + 1


class Sts(InstRunner):
    """
    Stores one byte from a Register to the data space. For parts with
    SRAM, the data space consists of the Register File, I/O memory,
    and internal SRAM (and external SRAM if applicable). For parts
    without SRAM, the data space consists of the Register File
    only. In some parts  the Flash memory has been mapped to the data
    space and can be written using this command. The EEPROM has a
    separate address space.

    A 7-bit address must be supplied. The address given in the
    instruction is coded to a data space address as follows:
    ADDR[7:0] = (~INST[8], INST[8], INST[10], INST[9], INST[3],
    INST[2], INST[1], INST[0])

    Memory access is limited to the address range 0x40...0xbf of the
    data segment.

    This instruction is not available in all devices. Refer to the
    device specific instruction set summary.

    Operation:
    (k) <= Rr

    Syntax:                Operands:                Program Counter:         
    STS k,Rr               16=<r=<31, 0=<k=<127       PC <= PC + 1

    16-bit Opcode:
    1010 1kkk rrrr kkkk

    Status register:
    N  Z  C
    -  -  -
    """
    def __init__(self):
        self.name = "Sts"
        self._mask = "1111111000000000"
        self._code = "0b1001001000000000"

    def execute(self, instr, state):
        # Convert instr to bin
        instr = bin(instr).replace("0b", "").zfill(16)

        # Extract memory adress k
        mem_k = ""
        for x in range(5,8):
            mem_k = mem_k + str(int(instr[x]))
        for x in range(12,16):
            mem_k = mem_k + str(int(instr[x]))
        mem_k = mem_k[0] +  mem_k # Add 8 number
        mem_k = int(mem_k, 2) # Convert to int

        # Extract register Rd
        reg_r = ""
        for x in range(7,12):
            reg_r = reg_r + str(int(instr[x]))
        reg_r = int(reg_r, 2) # Convert to int
        
        # Assign the result to the register
        state.data[mem_k] = state.data[reg_r]

        # Increments PC by 1
        state.pc = state.pc + 1


class Lds(InstRunner):
    """
    Loads one byte from the data space to a register. For parts with
    SRAM, the data space consists of the Register File, I/O memory,
    and internal SRAM (and external SRAM if applicable). For parts
    without SRAM, the data space consists of the register file
    only. In some parts the Flash memory has been mapped to the data
    space and can be read using this command. The EEPROM has a
    separate address space.

    A 7-bit address must be supplied. The address given in the
    instruction is coded to a data space address as follows:
    ADDR[7:0] = (~INST[8], INST[8], INST[10], INST[9], INST[3],
    INST[2], INST[1], INST[0])

    Memory access is limited to the address range 0x40...0xbf.

    This instruction is not available in all devices. Refer to the
    device specific instruction set summary.

    Operation:
    Rd <= (k)

    Syntax:                Operands:                Program Counter:         
    LDS Rd,k               16=<d=<31, 0=<k=<127     PC <= PC + 1

    16-bit Opcode:
    1010 0kkk dddd kkkk

    Status register:
    N  Z  C
    -  -  -
    """
    def __init__(self):
        self.name = "Lds"
        self._mask = "1111111000000000"
        self._code = "0b1001000000000000"

    def execute(self, instr, state):
        # Convert instr to bin
        instr = bin(instr).replace("0b", "").zfill(16)

        # Extract memory adress k
        mem_k = ""
        for x in range(5,8):
            mem_k = mem_k + str(int(instr[x]))
        for x in range(12,16):
            mem_k = mem_k + str(int(instr[x]))
        mem_k = mem_k[0] +  mem_k # Add 8 number
        mem_k = int(mem_k, 2) # Convert to int

        # Extract register Rd
        reg_d = ""
        for x in range(7,12):
            reg_d = reg_d + str(int(instr[x]))
        reg_d = int(reg_d, 2) # Convert to int

        # Assign the result to the register
        state.data[mem_k] = state.data[reg_d]

        # Increments PC by 1
        state.pc = state.pc + 1


class Rjmp(InstRunner):
    """
    Relative jump to an address within PC - 2K +1 and PC + 2K (words).
    For AVR microcontrollers with Program memory not exceeding 4K 
    words (8KB) this instruction can address the entire memory from
    every address location. See also JMP.

    Operation:
    PC <= PC + k + 1

    Syntax:                Operands:                Program Counter:         
    RJMP k                 K-2K=<k=<2K              PC <= PC + k + 1

    16-bit Opcode:
    1100 kkkk kkkk kkkk
    """
    def __init__(self):
        self.name = "Rjmp"
        self._mask = "1111000000000000"
        self._code = "0b1100000000000000"

    def execute(self, instr, state):
        # Extract k
        k = ""
        for x in range(4,16):
            k = k + str(int(instr[x]))
        k = int(k, 2) # Convert to int

        # Increments PC by k + 1
        state.pc = state.pc + k + 1


class Brbs(InstRunner):
    """
    Conditional relative branch. Tests a single bit in SREG and
    branches relatively to PC if the bit is set. This instruction 
    branches relatively to PC in either direction (PC - 63 ≤ 
    destination ≤ PC + 64). Parameter k is the offset from PC and is 
    represented in two’s complement form.

    Operation:
    If SREG(s)=1 then PC<=PC+k+1, else PC<=PC+1

    Syntax:                Operands:                Program Counter:         
    BRBS s,k               0=<s=<7, -64=<k=<63      PC <= PC + k + 1
                                                    PC <= PC + 1 
                                                    (if false)

    16-bit Opcode:
    1111 00kk kkkk ksss
    """
    def __init__(self):
        self.name = "Brbs"
        self._mask = "1111110000000000"
        self._code = "0b1111000000000000"

    def execute(self, instr, state):
        # Convert instr to bin
        instr = bin(instr).replace("0b", "").zfill(16)

        # Extract s
        s = str(int(instr[6]))
        for x in range(13,16):
            s = s + str(int(instr[x]))
        s = int(s, 2) # Convert to int

        # Extract k
        k = ""
        for x in range(6,13):
            k = k + str(int(instr[x]))
        k = int(k, 2) # Convert to int
        
        # Check if condition is true
        if state.flags[s]:
            state.pc = state.pc + k + 1
        else:
            # Increments PC by 1
            state.pc = state.pc + 1


class Brbc(InstRunner):
    """
    Conditional relative branch. Tests a single bit in SREG and 
    branches relatively to PC if the bit is cleared. This instruction
    branches relatively to PC in either direction (PC - 63 ≤
    destination ≤ PC +  64). Parameter k is the offset from PC and is 
    represented in two’s complement form.

    Operation:
    If SREG(s)=1 then PC<=PC+k+1, else PC<=PC+1

    Syntax:                Operands:                Program Counter:         
    BRBC s,k               0=<s=<7, -64=<k=<63      PC <= PC + k + 1
                                                    PC <= PC + 1 
                                                    (if false)

    16-bit Opcode:
    1111 01kk kkkk ksss
    """
    def __init__(self):
        self.name = "Brbc"
        self._mask = "1111110000000000"
        self._code = "0b1111010000000000"

    def execute(self, instr, state):
        # Convert instr to bin
        instr = bin(instr).replace("0b", "").zfill(16)

        # Extract s
        s = str(int(instr[6]))
        for x in range(13,16):
            s = s + str(int(instr[x]))
        s = int(s, 2) # Convert to int

        # Extract k
        k = ""
        for x in range(6,13):
            k = k + str(int(instr[x]))
        k = int(k, 2) # Convert to int
        
        # Check if condition is true
        if not state.flags[s]:
            state.pc = state.pc + k + 1
        else:
            # Increments PC by 1
            state.pc = state.pc + 1


class Nop(InstRunner):
    """
    This instruction performs a single cycle No Operation.

    Operation:
    No

    Syntax:                Operands:                Program Counter:         
    NOP                    None                     PC <= PC + 1

    16-bit Opcode:
    0000 0000 0000 0000

    Status register:
    N  Z  C
    -  -  -
    """
    def __init__(self):
        self.name = "Nop"
        self._mask = "1111111111111111"
        self._code = "0b0000000000000000"

    def execute(self, instr, state):
        # Increments PC by 1
        state.pc = state.pc + 1


class Break(InstRunner):
    """
    Add without Carry - Adds two registers without the C Flag and
    places the result in the destination register Rd.

    Operation:
    On-chip Debug system break.

    Syntax:                Operands:                Program Counter:         
    BREAK                  None                     PC <= PC + 1

    16-bit Opcode:
    1001 0101 1001 1000

    Status register:
    N  Z  C
    -  -  -
    """
    def __init__(self):
        self.name = "Break"
        self._mask = ""
        self._code = ""

    def match(self, instr):
        instr = int(instr)
        if instr == 38296:
            return True
        else:
            return False

    def execute(self, instr, state):
        raise BreakException


class In(InstRunner):
    """
    Loads data from the I/O Space (Ports, Timers, Configuration
    Registers, etc.) into register Rd in the Register File. When the
    port is 0x0, reads a character of the keyboard.
    
    Operation:
    Rd <= I/O (A)

    Syntax:                Operands:                Program Counter:         
    IN Rd,A                0=<d=<31, 0=<A=<63       PC <= PC + 1

    16-bit Opcode:
    1011 0AAd dddd AAAA

    Status register:
    N  Z  C
    -  -  -
    """
    def __init__(self):
        self.name = "In"
        self._mask = "1111100000000000"
        self._code = "0b1011000000000000"

    def execute(self, instr, state):
        # Convert instr to bin
        instr = bin(instr).replace("0b", "").zfill(16)

        # Extract Port A
        port_a = ""
        for x in range(6,7):
            port_a = port_a + str(int(instr[x]))
        for x in range(12,16):
            port_a = port_a + str(int(instr[x]))
        port_a = port_a[0] +  port_a  # Add 8 number
        port_a = int(port_a, 2) # Convert to int

        # Extract register Rd
        reg_d = ""
        for x in range(7,12):
            reg_d = reg_d + str(int(instr[x]))
        reg_d = int(reg_d, 2) # Convert to int

        # Check if port_a is 0x0 
        if port_a == 0:
            result = input("Input to R{}: ".format(reg_d))
            # Assign the result to the register
            state.data[reg_d] = result

        # Increments PC by 1
        state.pc = state.pc + 1


class Out(InstRunner):
    """
    Stores data from register Rr in the Register File to I/O Space
    (Ports, Timers, Configuration Registers, etc.). When the port is
    0x0 the exit is on base 10. When the port ins 0x1 the exit is on
    base 16. When the port is 0x2 the exit is UTF caracter.
    
    Operation:
    I/O (A) <= Rr

    Syntax:                Operands:                Program Counter:         
    OUT A,Rr               0=<d=<31, 0=<A=<63       PC <= PC + 1

    16-bit Opcode:
    1011 1AAr rrrr AAAA

    Status register:
    N  Z  C
    -  -  -
    """
    def __init__(self):
        self.name = "Out"
        self._mask = "1111100000000000"
        self._code = "0b1011100000000000"

    def execute(self, instr, state):
        # Convert instr to bin
        instr = bin(instr).replace("0b", "").zfill(16)

        # Extract Port A
        port_a = ""
        for x in range(6,7):
            port_a = port_a + str(int(instr[x]))
        for x in range(12,16):
            port_a = port_a + str(int(instr[x]))
        port_a = port_a[0] +  port_a  # Add 8 number
        port_a = int(port_a, 2) # Convert to int

        # Extract register Rd
        reg_d = ""
        for x in range(7,12):
            reg_d = reg_d + str(int(instr[x]))
        reg_d = int(reg_d, 2) # Convert to int

        # Check if port_a is 0x0 
        if port_a == 0:
            # Extract result from register
            result = int(state.data[reg_d])
            # Print result
            print "\nOutput from port {}: {}".format(hex(port_a), result)
        elif port_a == 1:
            # Extract result from register
            result = state.data[reg_d]
            # Print result
            print "\nOutput from port {}: {}".format(hex(port_a), result)
        elif port_a == 2:
            # Extract result from register
            result = unicode(str(state.data[reg_d]), "utf-8")
            # Print result
            print "\nOutput from port {}: {}".format(hex(port_a), result)

        # Increments PC by 1
        state.pc = state.pc + 1
