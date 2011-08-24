from __future__ import print_function

try:
    from simplelog import *
except ImportError:      
    import logging
    LOG_FORMAT = '[%(levelname)s] %(asctime)s: %(message)s'
    logging.basicConfig(format = LOG_FORMAT, level = logging.DEBUG, datefmt = '%H:%m:%S', filename="/tmp/simplelog.log", filemode="a+") 
    sl = logging.getLogger("simplelog")   
    sl.addHandler(logging.StreamHandler())
   
class PSException:
    def __init__(self, msg):
        self.msg = msg        

class PartialSolution:
    def __init__(self, grid = None):
        """
        Initiate a new sudoku partial solution
        """
        self.SIZE = 9
        self.BLOCK_SIZE = 3        
        self.grid = []            
        if grid == None:           
            #Set up 9 x 9 row 
            for i in xrange(9):     
                row = []
                for j in xrange(9):           
                    row.append(set(range(1,10)))
                self.grid.append(row)    
        else:
            self.grid = grid            
    
    def __str__(self):                         
        out = ""         
        acc = 0
        for i in xrange(self.SIZE):    
            line = []
            for j in xrange(self.SIZE):
                line.append(self.grid[i][j])
            out+=("{:^15}|{:^15}|{:^15}||{:^15}|{:^15}|{:^15}||{:^15}|{:^15}|{:^15}||\n".format(*line))            
            acc+=1                               
            if (acc % 3) == 0:                 
                out+= ("{:=^150}\n".format("="))                   
            else:
                out+= ("{:-^150}\n".format("-"))                    
        return out    
                
    def is_final(self):
        """
        Check if we have a final solution
        @return:
        true if possible solution space of all squares are 1, false otherwise
        """                              
        for i in xrange(self.SIZE):
            for j in xrange(self.SIZE):
                size = len(self.grid[i][j])
                if (size == 1):
                    continue
                else:
                    return False
        return True
        
    # 
    def is_dead_end(self):
        """
        Check if we have a dead end
        @return:
        true if possible solution space of all squares are 1, false otherwise
        """                              
        for i in xrange(self.SIZE):
            for j in xrange(self.SIZE):
                size = len(self.grid[i][j])
                if (size == 0):
                    return True
        return False
    def solve(self):
        """
        Solve sudoku puzzle
        @return:
        a partial solution or false if no solution can be found
        """                     
        print ("solving puzzle")   
        print(self)               
        if self.is_final():
            return self
        for i in xrange(self.SIZE):
            for j in xrange(self.SIZE):
                for k in xrange(1,9):
                    print("[debug]:trying new partial solution")                        
                    ps = PartialSolution(self.grid)      
                    size = len(ps.grid[i][j])       #only try inserting if size is greater than 1
                    if (size > 1):                  
                        ret = ps.set_element(i,j,k)                              
                        if (ret == False):          #leads to a dead end
                            continue                  
                        if (ps.is_dead_end()):
                            print ("[failure]: got a dead end")
                            continue
                        elif (ps.is_final()):     
                            print ("[success]: got a solution")
                            return ps
                        else:    
                            print (ps)
                            ret = ps.solve()
                            if (ret):
                                return ps                            
        return False                     
        
    def set_element(self, row, col, value):
        """
        Set an element in the puzzle
        @param:
        row - (int) row
        col - (int) column 
        value - (int) value       
        @return:
        True if elemenmts were set successfully or false on a bad entry  
        """                                            
        assert(row in range(10))
        assert(col in range(10))
        print(self)
                        
        if (value == 0):    #don't set 0 values
            return False 
            
        print("setting: ", row, col, value)            
        if not (value in self.grid[row][col]):
            print ("not a possible value")            
            return False
                    
        square = self.grid[row][col]
        square.clear()
        square.add(value)           
        
        print ("checking squares in same row")
        for i in xrange(self.SIZE):
            if (i != row):                         
                square = self.grid[i][col]
                size_init = len(square)
                try:
                    square.remove(value)
                except KeyError:                
                    pass
                size_fin = len(square)   
                print ("pos:({i},{col}), square:{square}, size:{size_fin}".format(**locals()))                
                if ((size_init == 2) & (size_fin == 1)):
                    print ("setting new value in row") 
                    self.set_element(i, col, next(square.__iter__())) #set element to be final element
                    
        #Get rid of all possible values in the same column
        print ("checking squares in same column")
        for j in xrange(self.SIZE):
            if (j != col):                         
                square = self.grid[row][j]
                size_init = len(square)
                try:
                    square.remove(value)
                except KeyError:            
                    pass
                size_fin = len(square)   
                print ("pos:({row},{j}), square:{square}, size:{size_fin}".format(**locals()))                
                if ((size_init == 2) & (size_fin == 1)):
                    print ("setting new value in column") 
                    self.set_element(row, j, next(square.__iter__())) #set element to be final element           
                    
        #Get rid of all possible values in the same block
        print ("checking squares in same block")
        for i in xrange(self.BLOCK_SIZE):
            for j in xrange(self.BLOCK_SIZE):
                block = (row/self.BLOCK_SIZE, col/self.BLOCK_SIZE)   
                b_row = i + (block[0] * self.BLOCK_SIZE)
                b_col = j + (block[1] * self.BLOCK_SIZE)                
                
                if ((b_row == row) & (b_col == col)):
                    print ("skipping current row & col")
                    continue
                    
                square = self.grid[b_row][b_col]
                size_init = len(square)
                try:
                    square.remove(value)  
                    print ("removing {value} from {b_row},{b_col}".format(**locals()))
                except KeyError:                                                      
                    print ("error removing")
                    pass
                size_fin = len(square)
                print ("pos:({b_row},{b_col}), square:{square}, size:{size_fin}".format(**locals()))                
                if ((size_init == 2) & (size_fin == 1)):
                    print ("setting new value in block") 
                    self.set_element(b_row, b_col, next(square.__iter__())) #set element to be final element     
        print(self)            
        return True
    #
    #
    
#
#      
def parse_text(textfile):       
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
    DEBUG = True    
    sl.debug("hello")    
    r = parse_text("sudoku.txt")  
    r2 = r[2]
    r2.solve()
   
        
        
        