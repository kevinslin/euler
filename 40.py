def p40():
	d = ""
	out = 1
	for i in range(5000000):
		d+=str(i)      
	for i in range(0, 7):
		index = pow(10, i)
		out*=int(d[index])
		print index
		print out		
	return out

print p40()