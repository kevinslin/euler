print """
It can be seen that the number, 125874, and its double, 251748, contain exactly the same digits, but in a different order.
Find the smallest positive integer, x, such that 2x, 3x, 4x, 5x, and 6x, contain the same digits.
"""                                                                                                                       


def convert_to_list(adigit):
    t = list(str(adigit))
    t.sort()
    return t

def main():                  
    i = 1
    while (True):
       one_i = convert_to_list(i)        
       two_i = convert_to_list(2 * i)          
       three_i = convert_to_list(3 * i)          
       four_i = convert_to_list(4 * i)          
       five_i = convert_to_list(5 * i)          
       six_i = convert_to_list(6 * i)             
       if (one_i == two_i == three_i == four_i == five_i == six_i):
           print "found answer: %d" % i
           return one_i 
       else:                 
           i+=1
           if ((i % 1000) == 0):
               print i
           continue     
    print "didn't find answer :("
    return 1
       
if __name__ == "__main__":       
    print "starting 52..."
    main()
   