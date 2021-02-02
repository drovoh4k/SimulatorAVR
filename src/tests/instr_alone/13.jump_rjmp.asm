values:
	LDI R16, 5
	LDI R17, 5
	RJMP end
	
substract:
	SUB R17, R16

end:
	ADD R17, R16
	BREAK