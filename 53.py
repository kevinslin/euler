import copy

def show_prompt():    
    print """
    If we take 47, reverse and add, 47 + 74 = 121, which is palindromic.

    Not all numbers produce palindromes so quickly. For example,

    349 + 943 = 1292,
    1292 + 2921 = 4213
    4213 + 3124 = 7337

    That is, 349 took three iterations to arrive at a palindrome.

    Although no one has proved it yet, it is thought that some numbers, like 196, never produce a palindrome. A number that never forms a palindrome through the reverse and add process is called a Lychrel number. Due to the theoretical nature of these numbers, and for the purpose of this problem, we shall assume that a number is Lychrel until proven otherwise. In addition you are given that for every number below ten-thousand, it will either (i) become a palindrome in less than fifty iterations, or, (ii) no one, with all the computing power that exists, has managed so far to map it to a palindrome. In fact, 10677 is the first number to be shown to require over fifty iterations before producing a palindrome: 4668731596684224866951378664 (53 iterations, 28-digits).

    Surprisingly, there are palindromic numbers that are themselves Lychrel numbers; the first example is 4994.

    How many Lychrel numbers are there below ten-thousand?

    NOTE: Wording was modified slightly on 24 April 2007 to emphasise the theoretical nature of Lychrel numbers.
    """
             
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
    
def t_reverse_digit():
    t1 = reverse_digit(10)    
    print type(t1)    
    
def t_is_palindrome():
    print "testing is_palindrome..."
    t1 = is_palindrome(10)
    t2 = is_palindrome(101)    
    assert (t1 == False)
    assert (t2 == True)    
    print "all test passed"
    
        
def main():
    "solving euler 53..."
    l_numbers = 0
    for i in xrange(1, 10000, 1):  
        if ((i % 1000) == 0):   #show progress
            print i                                       
        t = reverse_digit(i)  
        s = i + t 
        # print "==="            
        # print i 
        # print t
        # print s      
        
        acc = 1
        while acc < 50:    
            if (is_palindrome(s)):               
                break
            else:                                   
                # print "old: %d" % s                 
                t = reverse_digit(s)             
                # print "reverse: %d" % t               
                s = s + t
                acc += 1                          
                # print "new: %d\n acc: %d" % (s, acc)                                                
        if ( acc >= 50):
            l_numbers += 1
            print "===="
            print i    
            print s
            print acc       
    print "lnumbers: %s" % l_numbers            
    return l_numbers            
        
        
    


if __name__ == "__main__":
    main()