import re                  
import simplelog

sample = """
Grid 01
003020600
900305001
001806400
008102900
700000008
006708200
002609500
800203009
005010300   
"""

def parse_puzzle(puzzle):
    """
    Parse sudoku puzzle into lists of horizontal bars
    @param:                 
    puzzle - 9 x 9 sudoku board optionally prefaced by a title
    @return:
    a lists of horizontal fields of sudoku puzzle
    """
    puzzle = re.sub("\sGrid \d{2}","", sample)
    puzzle = puzzle.strip().split("\n")              
    return puzzle
    

import inspect
sl = simplelog.SimpleLog()

def foo(arg1, arg2, *args, **kwargs):
    frame = inspect.currentframe()
    values = inspect.getargvalues(frame)
    info = inspect.getframeinfo(frame)
    return values, info

def enter(function):
    def decorator(*args, **kwargs):
        print("entering function")
        frame = inspect.currentframe()
        values = inspect.getargvalues(frame)
        info = inspect.getframeinfo(frame)
        loc = values[3]
        func_name = loc['function'].func_name
        args = loc ['args']
        print (func_name, args)
        return function(*args, **kwargs)
    return decorator

@sl.enter
def bar(arg1, arg2, *args):
    print arg1, arg2
    return




    
