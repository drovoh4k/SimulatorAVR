boolean_or:
    LDI R16, 0b00000011 ; Set 1 to R16
    LDI R17, 0b00000101 ; Set 1 to R17
    OR R17, R16
    BREAK