values:
	LDI R16, 6
	LDI R17, 5
	SUB R16, R17
	BRBC 1, end ; If ZERO=0
	
ldi:
	LDI R18, 14

end:
	BREAK