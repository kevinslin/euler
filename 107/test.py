import graph

def make_g2():
    g = graph.Graph()

    ### Add Nodes
    for n in range(12):
        g.add_node(n)

    ### Add Edges
    g[0] = {1: 3, 2: 5, 3: 4}
    g[1] = {0: 3, 4: 3, 5: 6}
    g[2] = {0: 5, 3: 2, 6: 4}
    g[3] = {0: 4, 2: 2, 4: 1, 7: 5}
    g[4] = {1: 3, 3: 1, 5: 2, 8: 4}
    g[5] = {1: 6, 4: 2, 9: 5}
    g[6] = {2: 4, 7: 3, 10: 6}
    g[7] = {3: 5, 6: 3, 8: 6, 10: 7}
    g[8] = {4: 4, 7: 6, 9: 3, 11: 5}
    g[9] = {5: 5, 8: 3, 11: 9}
    g[10] = {6: 6, 7: 7, 11: 8}
    g[11] = {8: 5, 9: 9, 10: 8}

    g.validate()
    
    return g
    