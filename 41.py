import sys

def prime_gen(maxPrime, numPrime = sys.maxint):
	"""
	Generate a list of primes
	@param:
	maxPrime - max prime number generated
	numPrime - max number of primes generated
	""" 
	acc = 2
	S = []
	P = []  
	S = range(maxPrime)
	S.remove(0)
	S.remove(1)
	S.remove(2)

	while S != []:
		for j in S: 
			if (j % acc == 0):
				S.remove(j)
		t = S.pop(0)           
		print t
		P.append(str(t))
		acc = t	
	return S, P	

def isPan(n):
	"""
	Check if number is pandigital
	@param:
	n - input
	@return:
	True if pandigital and False otehrwise
	"""                                   
	P = set()
	V = set()
	for i in range(1,len(n)+1):
		P.add(str(i))

	# print "n: {0}".format(n) 	                 
	for i in n:
		# print "P:{P}\nV:{V}".format(**locals())
		if i in V:
			print "i is in V"
			return False
		else:
			V.add(i)
			if i in P:
				P.discard(i)
			else:       
				print "i is not in P"
				return False	
	return True

def p41():
	primes = prime_gen(99999999)
	print primes 
	
	while (True):
		prime = primes.pop(-1) 		
		flag = isPan(prime)
		if (flag):
			return prime
		if (prime == 3):
			return False
				
	
def t_prime_gen():
	print "testing prime_gen"
	t1 = prime_gen(20)		
	print t1
	
def t_isPan():
	print "testing isPan"
	t1 = isPan(str(1))      
	t2 = isPan(str(12))	
	t3 = isPan(str(123))    
	t4 = isPan(str(123456789))    
	t5 = isPan(str(162345978))

	nt1 = isPan(str(2))
	nt2 = isPan(str(13))
	nt3 = isPan(str(141))
	nt4 = isPan(str(1233))
	nt5 = isPan(str(12345673))
	
	assert(t1 == True)
	assert(t2 == True)
	assert(t3 == True)
	assert(t4 == True)
	assert(t5 == True)
	
	assert(nt1 == False)	
	assert(nt2 == False)
	assert(nt3 == False)
	assert(nt4 == False)
	assert(nt5 == False)			
	
	print "all test passed"

# t_prime_gen()	          
# t_isPan()  
p41()


