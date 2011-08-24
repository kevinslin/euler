import copy
import graph
import graphutil
import numpy      
import random
import sys

def prepare_graph(filename):
    """Create a python readable adjacency list"""
    fh = open(filename, "r+")
    fh_temp = open(filename, "r+")  #TODO: hack until i figure out a better way of doing this
    
    size = len(fh_temp.readline().split(","))
    adj_list = numpy.zeros((size, size))
    
    for i in xrange(size):   
        row = fh.readline().strip("\n").split(",")
        for j in xrange(size):
            v = row[j].strip()            
            if (v.strip() == "-"):  #convert - to 0
                v = 0                
            adj_list[i, j] = v    
    return adj_list

def make_graph(adj_list):   
    """Makes a graph given an adjacency list"""
    g = graph.Graph() 
    print adj_list
    for row in enumerate(adj_list):
        for col in enumerate(row[1]):
            g.add_edge(row[0], col[0], col[1])
            # print "(" + str(row[0]) + "," + str(row[0]) + ")"
            # print "(" + str(row[0]) + "," + str(col[0]) + ")"
            # print "distance: " + str(col[1])                 
    g.validate()        
    return g

def make_min_span_tree(g):
    """Make a minimal spanning tree given graph g"""               
    nodes_max = len(g.nodes())    
    nodes_num = 1        
    BASE = 65
    
    T = graph.Graph()
    V = set()
    n = random.choice(g.nodes())    #pick random node to start with        
    T.add_node(n)       
    print "choose node: {n}".format(**locals()) 
       
    while nodes_num < nodes_max: 
        n_new = None
        n_old = None
        min_dist = sys.maxint
        
        for n2 in T.nodes():
            for h in g[n2].keys():  #get neighbors of current node
                if h in T.nodes():  #skip nodes we already have
                    continue                                           
                new_dist = g[n2][h]                
                if new_dist == 0:   #skip invalid edges
                    continue       
                print "checking edge({n2},{h}) with distance {new_dist}".format(**locals())             
                if (new_dist < min_dist):   #found new minimal distance
                    print "found new min_dist: edge({n2},{h}) with distance {new_dist}".format(**locals())
                    min_dist = new_dist
                    n_new = h
                    n_old = n2                                    
        T.add_node(n_new)
        T.add_edge(n_old, n_new, min_dist)
        nodes_num+=1
        print "num nodes:{nodes_num}\nadd new node: {n_new}\ndist:{min_dist}\n===".format(**locals())  
    return T

#
def get_edge_weight(g):
    """Sum the weight of all edges in a graph"""    
    total = 0                    
    V = set()
    for n in g.nodes():
        for h in g[n].keys():
            edge = frozenset((n,h))
            if edge in V:
                continue
            else:
                total += g.get_edge_attr(n,h)    
                V.add(edge)                
    return total
    
 
def main():    
    #Test case
    # adj_list = prepare_graph("network2.txt")
    # g_test = make_graph(adj_list)
    # w1_o = get_edge_weight(g_test)
    # assert(g_test.get_edge_attr(0, 0) == 0)
    # assert(g_test.get_edge_attr(0, 3) == 21)
    # assert(g_test.get_edge_attr(2, 3) == 28)         
    # tree1 = make_min_span_tree(g_test)
    # w1 = get_edge_weight(tree1)  
    # print w1_o
    # print w1
    
    adj_list = prepare_graph("network.txt")
    g = make_graph(adj_list)
    w_orig = get_edge_weight(g)
    min_tree = make_min_span_tree(g)
    w_final = get_edge_weight(min_tree)
    diff = w_final - w_orig
    print w_orig
    print w_final
    print diff
    
    
    # dist, pred = shortest_weighted_paths(g_test, 0)

    
    


if __name__ == "__main__":
    main()        