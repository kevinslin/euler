

def p48():
	total = 0         
	ceiling = pow(1000,1000)  
	i = 1
	
	while (i != 1000): 
		if (i % 10 == 0): #progress
			print i
		total += pow(i, i) #total
		total %= pow(10, 10)  #last ten digits
		i+=1
	return total
	
print p48()		