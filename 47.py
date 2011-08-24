from utils import *

DEBUG = True                 

def p47(ceiling):
	"""
	Find first four consecutive integers to have four
	distince prime factors
	@param:
	ceiling - limit for product of primes
	@return
	first four consecutive integers to have four distinct prime factors
	"""                                                                
	P = prime_gen(ceiling + 30)
	S = {}   
	T = set() 	#set of primes
	out = []
	                      
	#Note: base value of tag is equal to initial value 
	S[0]={'index':0,'base':0}
	S[1]={'index':1,'base':1}
	S[2]={'index':2,'base':2}
	slot_curr = 2	#current tag   
	slot_init = 2   #max amount of tags
	acc = 0
	print P
	print S 
	
	while True:    
		acc+=1 
		l = P[S[0]['index']]
		m = P[S[1]['index']]
		r = P[S[2]['index']]
		total = l * m * r	 		
		print "l:{l},m:{m},r:{r},t:{total}".format(**locals())

		
		if (total <= ceiling):
			if ((l == m) | (l == r) | (m == r)):	#skip non-distince primes
				S[slot_curr]['index']+=1   
				print "skipping"
				continue            	   
				
			T.add(total) 		#add new total     			
			out.append(total)     
			
			# p = 2   
			# while (True):
			# 	l = P[S[0]['index']]
			# 	m = P[S[1]['index']]
			# 	r = P[S[2]['index']]
			# 	total = l * m * r	 		          #check that the sum doesn't go over 
			# 	
			# 	r = pow(r, power)
			# 	
			# 	if (total <= ceiling):
			# 		T.add(total)
			# 		out.append(total)
			# 		p+=1		    	
								
			S[slot_curr]['index']+=1
			
		#                     
		else:
			while (total > ceiling):
				print "slot_cur:{slot_curr}".format(**locals())       
				slot_curr-=1
				if (slot_curr < 0):
					out.sort()     
					print len(out)
					print len(T)     
					print "acc:{acc}".format(**locals())
					print "done"
					return out  
				else:
					S[slot_curr]['index']+=1	#increase current slot                 
					S[slot_curr+1]['base']=	S[slot_curr]['index'] 	#optimization: skip already explored permutations					
					S[slot_curr+1]['index'] = S[slot_curr+1]['base'] #reset previous slot to new base			
							
					total = P[S[0]['index']] * P[S[1]['index']] * P[S[2]['index']] #check that the sum doesn't go over 
					print "increased slot{slot_curr}. total is: {total}".format(**locals())
			slot_curr = slot_init

print p47(700)	      


	