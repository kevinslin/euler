from __future__ import print_function

try:
    from simplelog import *
except ImportError:      
    import logging
    LOG_FORMAT = '[%(levelname)s] %(asctime)s: %(message)s'
    logging.basicConfig(format = LOG_FORMAT, level = logging.DEBUG, datefmt = '%H:%m:%S', filename="/tmp/simplelog.log", filemode="a+") 
    sl = logging.getLogger("simplelog")   
    sl.addHandler(logging.StreamHandler())
    
   
def parse_puzzle():       
    """
    Solves sudoku puzzle
    @param:
    textfile - sudoku file
    @return:
    sol - an array containing the solutions to the sudoku puzzle
    """
    sol = []
    with open(textfile, "r") as fh:                                             
        acc = 0                                   
        ps = None          
        line = True            
        while (line):                                                       
            line = fh.readline()
            if line.startswith("Grid"):      #Found a new grid
                sol.append(ps)
                ps = PartialSolution()
                col = 0                 
                continue         
            else:      
                print (line, col)                
                for row, value in enumerate(line):
                    ps.set_element(int(col), int(row), int(value)) 
                    if (row >= 8):                          #ignore \r\n symbols
                        if (DEBUG): #TEMP
                            if len(sol) == 3:
                                return sol
                        break
                col +=1                             
    return sol[1:]
    

if __name__ == "__main__":
    print "solving 96...."