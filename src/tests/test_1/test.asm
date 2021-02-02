aritmetic_adc:
    LDI R16, 0b11111111 ; Set 1 to R16
    LDI R17, 1 ; Set 1 to R17
	LDI R18, 2
	LDI R19, 3
    ADD R17, R16 ; CARRY = 1
	ADC R18, R19
    BREAK