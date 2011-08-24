"""
TODO:
- don't need to but should convert data to uppercase or lower case (NEVER TRUST INPUT)
- reverse the triangular number if letters go out of bounds

"""

CHAR_OFFSET = 64 # "A" starts at 65

def p42():          	
	fh = open("words.txt", "r")	
	words = fh.read() 
	words = words.split(",")
	total = 0         
	t = gen_t_number(1000)
	m = 1000	 #max triangular number   
	
	for word in words:
		word = word.strip("\"")		
		print word    
		sum = 0
		
		for l in word:
		   sum+=ord(l) - CHAR_OFFSET 
		
		if sum in t:
			total+=1
		if sum > m:
			print "error, sum out of bounds"
			return 
	return total			
		
		

			
	
def gen_t_number(m):
	"""
	Generate triangular numbres
	@param
	m - max totla
	@return:
	set of triangular numbers
	"""                      
	t = set()
	c = 0         
	n = 0	
	while (c < m):
		c = (0.5 * n) * (n + 1.0)
		t.add(c)
		n+=1
	return t		   

print p42()	

