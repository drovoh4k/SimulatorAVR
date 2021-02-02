values:
	LDI R16, 5
	LDI R17, 5
	SUB R16, R17
	BRBS 1, end ; If ZERO=1
	
ldi:
	LDI R18, 14

end:
	BREAK