#!/usr/bin/env python
# -*- coding: utf-8 -*-

class BitVector(object):
    """
    Represents a binary word of a certain size, but less or equal to
    16 bits unsigned.

    :param _w: Codec the value of BitVector
    :type _w: int, private
    """
    def __init__(self, w=0):
        self._w = w
    
    def extract_field_u(self, mask):
        """
        Apply a mask over the self and extract the selected bits. The
        result is an unsigned value.

        For example:
            self   - 0b10100110
            mask   - 0b00110011
            result - 0b00001010

        :param mask: Binary mask
        :type mask: integrer, binary

        :return: Postive integrer
        :rtype: int
        """
        # Generate binary from self._w
        self_bin = bin(self._w).replace("0b", "").zfill(self.__len__())

        mask = mask.zfill(self.__len__())
        
        # Apply the mask
        result_bin = ""
        for x in range(self.__len__()):
            result_bin = result_bin + str(int(self_bin[x]) & int(mask[x]))
        result_bin = "0b" + result_bin.zfill(self.__len__())

        return result_bin


    def extract_field_s(self, mask):
        """
        Apply a mask over the seld and extract selected bits. The
        result is a signed value.
        
        :param mask: Binary mask
        :type mask: 

        :return: Postive or negative integrer
        :rtype: int
        """
        pass

    def __int__(self):
        return self._w

    def __index__(self):
        self_bin = bin(self._w).replace("0b", "")
        return int(self_bin, 2)
        
    def __repr__(self):
        my_hex = hex(self._w)[2:].upper() # Generate Hex number
        if len(my_hex) != len(str(self._w)): # To be the same len
            my_hex = "0" + my_hex
        return my_hex

    def __add__(self, o):
        if type(o) is int: # o is an int
            add = int(self._w) + o
            return self.__class__(add)
        elif isinstance(o, object):# o is an object
            add = int(self._w) + int(o._w)
            return self.__class__(add)

    def __sub__(self, o):
        if type(o) is int: # o is an int
            sub = int(self._w) - o
            return self.__class__(sub)
        elif isinstance(o, object): # o is an object
            sub = int(self._w) - int(o._w)
            return self.__class__(sub)

    def __and__(self, o):
        vector_1 = str(bin(self._w).replace("0b", "")).zfill(16) # Refill with 0
        vector_2 = str(bin(o._w).replace("0b", "")).zfill(16) # Refill with 0
        
        result = ""
        for x in range(16):
            result = result + str(int(vector_1[x]) & int(vector_2[x]))
        result = int(result, 2) # Convert bin to int

        return self.__class__(result)

    def __or__(self, o):
        vector_1 = str(bin(self._w).replace("0b", "")).zfill(16) # Refill with 0
        vector_2 = str(bin(o._w).replace("0b", "")).zfill(16) # Refill with 0
        
        result = ""
        for x in range(16):
            result = result + str(int(vector_1[x]) | int(vector_2[x]))
        result = int(result, 2) # Convert bin to int

        return self.__class__(result)

    def __xor__(self, o):
        vector_1 = str(bin(self._w).replace("0b", "")).zfill(16) # Refill with 0
        vector_2 = str(bin(o._w).replace("0b", "")).zfill(16) # Refill with 0
        
        result = ""
        for x in range(16):
            result = result + str(int(vector_1[x]) ^ int(vector_2[x]))
        result = int(result, 2) # Convert bin to int

        return self.__class__(result)

    def __invert__(self):
        vector = str(bin(self._w).replace("0b", "")) # Extract 0b
        vector = vector.zfill(len(vector))
        
        result = ""
        for x in vector:
            if x == "0":
                result = result + "1"
            elif x == "1":
                result = result + "0"
        result = int(result, 2) # Convert bin to int
        return self.__class__(result)

    def __lshift__(self, i):
        num = int(self._w)
        bits = 8
        try:
            for x in range(i):
                num <<= 1
                if(bits):
                    num |= 1
                num &= (2**bits-1)
            return Byte(num)
        
        except IndexError:
            raise IndexError
            
    def __rshift__(self, i):
        num = int(self._w)
        bits = 8
        try:
            for x in range(i):
                num &= (2**bits-1)
                bit = num & 1
                num >>= 1
                if(bit):
                    num |= (1 << (bits-1))
            return Byte(num)
        
        except IndexError:
            raise IndexError

    def __eq__(self, o):
        vector_1 = str(bin(self._w).replace("0b", "")) # Extract 0b
        vector_2 = str(bin(o._w).replace("0b", "")) # Extract 0b

        if vector_1 == vector_2:
            return True
        else:
            return False

    def __getitem__(self, i):
        vector = str(bin(self._w).replace("0b", "")) # Extract 0b
        vector = vector.zfill(self.__len__())
        try:
            if vector[i] == '0':
                return False
            elif vector[i] == '1':
                return True
        except IndexError:
            raise KeyError

    def __setitem__(self, i, v):
        vector = str(bin(self._w).replace("0b", "")) # Extract 0b
        vector = vector.zfill(self.__len__())
        vector = list(vector)
        try:
            vector[i] = v
            vector = self.__class__(int("".join(map(str,vector)), 2))
            self._w = int(vector)
        except IndexError:
            raise KeyError
                

class Byte(BitVector):
    """
    Represents a word of 8 bits
    """
    def __len__(self):
        return 8

    def __concat__(self, b):
        """
        Concatatenate self with Byte b. Self is MSB and b is LSB.

        :param b: Other byte
        :type b: object

        :return: Word class 
        :rtype: object
        """
        vector_1 = str(bin(self._w).replace("0b", "")).zfill(8) # Extract 0b
        vector_2 = str(bin(b._w).replace("0b", "")).zfill(8) # Extract 0b

        result = int(vector_1 + vector_2, 2)

        return Word(result)


class Word(BitVector):
    """
    Represent a word of 16 bits
    """
    def __len__(self):
        return 16

    def lsb(self):
        """
        Return the less significant byte
        """
        list_self = bin(self._w).replace("0b", "") # Binary without 0b
        list_self = list_self.zfill(16) # Fill with 0s
        list_self = list(list_self) # Generate the list
        result = "".join(list_self[8:self.__len__()]) # To str
        result = int(result, 2) # Convert to int
        return self.__class__(result)
        
    def msb(self):
        """
        Return the most significant byte
        """
        list_self = bin(self._w).replace("0b", "") # Binary without 0b
        list_self = list_self.zfill(16) # Fill with 0s
        list_self = list(list_self) # Generate the list
        result = "".join(list_self[0:8]) # To str
        result = int(result, 2) # Convert to int
        return self.__class__(result)
