import sys

def prime_gen(maxPrime):
	"""
	Generate a list of primes
	@param:
	maxPrime - max prime number generated   
	@return:
	sorted list of primes
	""" 
	S = []
	P = []     
	#Generate numbers up to maxprime
	S = range(maxPrime)
	S.remove(1)	 	
	acc = 2            

	while S != []:
		for j in S: #BUG: unkown behavior. Skips 2 in interation (?)
			if (j % acc == 0):
				S.remove(j)
		t = S.pop(0)           
		P.append(t)
		acc = t	
	return P      

def reverse_digit(adigit):
    """
    @param:
    adigit - a digit 
    @return:
    (long) the reversed adigit
    @notes:
    will chop of leading zeroes 
    eg. 00001 will return 1
    """                       
    from copy import deepcopy
    
    t = repr(adigit)    
    if (type(adigit) == long):  #chop of "L" 
        t=t[:-1]            
    t = t[::-1]
    t = ''.join(t)    
    return long(t)

def is_palindrome(adigit):
    """
    returns true if digit is a palindrome
    """             
    t = adigit
    t2 = reverse_digit(adigit)           
    return t == t2   
####################################    
def t_reverse_digit():
    print "testing reverse digit..."
    t1 = reverse_digit(10)    
    print type(t1)    
    
def t_is_palindrome():
    print "testing is_palindrome..."
    t1 = is_palindrome(10)
    t2 = is_palindrome(101)    
    assert (t1 == False)
    assert (t2 == True)    
    print "all test passed"	

def t_prime_gen():
	print "testing prime_gen"
	t1 = prime_gen(50)			
	print t1                
	
	
	
