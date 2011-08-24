import collections
import types

def loads(repstr):
    """
    Return a new graph initialized by the contents of the string
    repstr.  The string should contain the representation generated by
    a call to dumps.
    """
    return eval(repstr)

def load(f):
    """
    Return a new graph initialized by the contents of the file f.  The
    file should contain the representation generated by a call to
    dump.
    """
    return loads(f.read())

class BaseGraph:
    """
    Abstract graph class that supports node and edge attributes.
    """

    ### Graph structure:
    ###
    ###  g = {node: _nodetup}
    ###  _nodetup = (attr, nbrs)
    ###  nbrs = {node: attr}
    _nodetup = collections.namedtuple('node', 'attr nbrs')

    def __init__(self):
        """
        Create an empty graph.
        """
        self._nodes = {}

    def __len__(self):
        """
        Return the number of nodes in the graph (len(g) == g.node_count()).
        """
        return self.node_count()

    def __contains__(self, node):
        """
        Returns true if node is in the graph, false otherwise.
        """
        return self.has_node(node)

    def __iter__(self):
        """
        Create an iterator over the nodes in the graph.
        """
        return self._nodes.__iter__()

    def __getitem__(self, node):
        """
        Return the neighbor dictionary for the node. 

        nbrs = g[k] is the same as nbrs = g.get_neighbors(k)
        """
        return self.get_neighbors(node)

    def __setitem__(self, node, nbrs):
        """
        Set the neighbor dictionary for the node.

        g[k] = nbrs is the same as g.set_neighbors(k, nbrs)
        """
        self.set_neighbors(node, nbrs)

    def _repstr(self):
        """
        Helper function for __str__ that returns a string of the
        internal graph representation.
        """
        return str(self._nodes)

    def _reprepr(self):
        """
        Helper function for __repr__ that returns a string of the
        internal graph representation that can be evaluated to
        recreate the representation.
        """
        s = self._repstr()
        s = s.replace('node(', 'BaseGraph._nodetup(')
        return s

    def nodes(self):
        """
        Returns a list of nodes in the graph.
        """
        return self._nodes.keys()

    def get_neighbors(self, node):
        """
        Returns the neighbor dictionary {neighbor node: attr} for node
        or raises a KeyError if node is not in the graph.
        """
        return self._nodes[node].nbrs

    def set_neighbors(self, node, neighbors):
        """
        Set the neighbor dictionary for the node.  Add node if it's
        not in the graph.

        Example: 
        g[0] = {1: None} -- node 0 has 1 neighbor (node 1)
                            and there is no edge attribute.
        """
        if self.has_node(node):
            if type(neighbors) != types.DictType:
                raise TypeError("neighbors must be a dictionary, not " + type(neighbors).__name__)
            self._nodes[node] = BaseGraph._nodetup(self._nodes[node].attr, neighbors)
        else:
            self._nodes[node] = BaseGraph._nodetup(None, neighbors)

    def get_node_attr(self, node):
        """
        Returns the attribute for node or raises KeyError if node is
        not in the graph.
        """
        return self._nodes[node].attr

    def set_node_attr(self, node, attr):
        """
        Sets the attribute for node to attr or raises KeyError if node
        is not in the graph.
        """
        if self.has_node(node):
            self._nodes[node] = Graph._nodetup(attr, self._nodes[node].nbrs)
        else:
            raise KeyError(node)        

    def get_edge_attr(self, u, v):
        """
        Returns the attribute for edge (u, v) or raises KeyError if
        the edge is not in the graph.
        """
        return self._nodes[u].nbrs[v]

    def set_edge_attr(self, u, v, attr):
        """
        Sets the attribute for edge (u, v) to attr or raises KeyError
        if edge is not in the graph.

        Must be overriden by subclasses
        """
        raise NotImplementedError

    def node_count(self):
        """
        Returns the number of nodes in the graph.
        """
        return len(self._nodes)

    def edge_count(self):
        """
        Returns the number of edges in the graph.

        Must be overriden by subclasses.
        """
        raise NotImplementedError

    def add_node(self, node, attr = None):
        """
        Add node to the graph with optional attribute attr.  Does
        nothing if node is already in the graph.
        """
        if not self.has_node(node):
            self._nodes[node] = Graph._nodetup(attr, {})

    def add_edge(self, u, v, attr = None):
        """
        Add edge (u, v) to the graph with optional attribute attr.
        If nodes u or v are not in the graph, they will be added.

        Must be overriden by subclasses.
        """
        raise NotImplementedError

    def remove_node(self, node):
        """
        Remove node from the graph, if it exists.  Raises KeyError if
        node is not in the graph.
        """
        self._nodes.pop(node)
        for k, nk in self._nodes.iteritems():
            nk.nbrs.pop(node, None)

    def remove_edge(self, u, v):
        """
        Remove edge from the graph, if it exists.

        Must be overriden by subclasses.
        """
        raise NotImplementedError
        
    def has_node(self, node):
        """
        Returns True if node is in the graph, False otherwise.
        """
        return node in self._nodes

    def has_edge(self, u, v):
        """
        Returns True if edge (u, v) is in the graph, False otherwise.
        """
        return (v in self._nodes[u].nbrs)

    def dumps(self):
        """
        Return a string representation of the graph that can 
        be used by loads to recreate the graph.

        Must be overriden by subclass.
        """
        raise NotImplementedError

    def dump(self, f):
        """
        Store a string representation to the file f that can be read
        by load to recreate the graph.
        """
        f.write(self.dumps())

    def validate(self):
        """
        Validates that the graph structure is consistent.  Raises
        UserWarning if inconsistent, does nothing otherwise.

        Should be overriden by subclasses.
        """
        raise UserWarning('unable to validate graph - no validate method')


class DiGraph(BaseGraph):
    """
    Directed graph class that supports node and edge attributes.
    """

    def __init__(self, graphrepr = None):
        """
        Create a new DiGraph.  

        If the optional graphrepr argument is not provided the graph
        will be empty.  Otherwise, graphrepr will be used as the
        internal representation and will be validated.  The graphrepr
        argument should primarily be used by load or loads.
        """
        BaseGraph.__init__(self)
        if graphrepr:
            self._nodes = graphrepr
            self.validate()

    def __str__(self):
        """
        Return a string representation of the graph.
        """
        return 'DiGraph(' + self._repstr() + ')'

    def edge_count(self):
        """
        Returns the number of edges in the graph.
        """
        edges = 0
        for n in self._nodes:
            edges += len(self._nodes[n].nbrs)
        return edges
    
    def set_edge_attr(self, u, v, attr):
        """
        Sets the attribute for edge (u, v) to attr or raises KeyError
        if edge is not in the graph.
        """
        if self.has_node(u):
            if v in self._nodes[u].nbrs:
                self._nodes[u].nbrs[v] = attr
            else:
                raise KeyError(v)
        else:
            raise KeyError(u)        

    def add_edge(self, u, v, attr = None):
        """
        Add edge (u, v) to the graph with optional attribute attr.
        If nodes u or v are not in the graph, they will be added.
        """
        if not self.has_node(u):
            self.add_node(u)
        if not self.has_node(v):
            self.add_node(v)
        self._nodes[u].nbrs[v] = attr

    def remove_edge(self, u, v):
        """
        Remove edge from the graph, if it exists.
        """
        if self.has_node(u):
            self._nodes[u].nbrs.pop(v, None)

    def dumps(self):
        """
        Return a string representation of the graph that can 
        be used by loads to recreate the graph.
        """
        return 'DiGraph(' + self._reprepr() + ')'

    def validate(self):
        """
        Validates that the graph structure is consistent.  If node a
        is a neighbor of node b, then node a must be a node in the
        graph.  If this holds for all neighbors, then do nothing.  If
        not, raises a UserWarning.
        """
        for n, nt in self._nodes.iteritems():
            for nbr in nt.nbrs:
                if nbr not in self._nodes:
                    # Missing node
                    msg = ('node ' + str(n) + ' has a neighbor (' +
                           str(nbr) + ') that is not a node in the graph')
                    raise UserWarning(msg)

class Graph(BaseGraph):
    """
    Undirected graph class that supports node and edge attributes.
    """

    def __init__(self, graphrepr = None):
        """
        Create a new Graph.  

        If the optional graphrepr argument is not provided the graph
        will be empty.  Otherwise, graphrepr will be used as the
        internal representation and will be validated.  The graphrepr
        argument should primarily be used by load or loads.
        """
        BaseGraph.__init__(self)
        if graphrepr:
            self._nodes = graphrepr
            self.validate()

    def __str__(self):
        """
        Return a string representation of the graph.
        """
        return 'Graph(' + self._repstr() + ')'

    def edge_count(self):
        """
        Returns the number of edges in the graph.
        """
        edges = 0
        for n in self._nodes:
            edges += len(self._nodes[n].nbrs)
        return edges / 2

    def set_edge_attr(self, u, v, attr):
        """
        Sets the attribute for edge (u, v) to attr or raises KeyError
        if edge is not in the graph.
        """
        if v not in self._nodes[u].nbrs:
            raise KeyError(v)
        if u not in self._nodes[v].nbrs:
            raise KeyError(u)

        self._nodes[u].nbrs[v] = attr
        self._nodes[v].nbrs[u] = attr

    def add_edge(self, u, v, attr = None):
        """
        Add edge (u, v) to the graph with optional attribute attr.
        If nodes u or v are not in the graph, they will be added.
        """
        if not self.has_node(u):
            self.add_node(u)
        if not self.has_node(v):
            self.add_node(v)
        self._nodes[u].nbrs[v] = attr
        self._nodes[v].nbrs[u] = attr

    def remove_edge(self, u, v):
        """
        Remove edge from the graph, if it exists.
        """
        if self.has_node(u) and self.has_node(v):
            self._nodes[u].nbrs.pop(v, None)
            self._nodes[v].nbrs.pop(u, None)

    def dumps(self):
        """
        Return a string representation of the graph that can 
        be used by loads to recreate the graph.
        """
        return 'Graph(' + self._reprepr() + ')'

    def validate(self):
        """
        Validates that the graph structure is consistent.  If node a
        is a neighbor of node b, then node b must be a neighbor of
        node a and they must both have the same attribute.  If this
        holds for all neighbors, then do nothing.  If not, raises a
        UserWarning.
        """
        for n, nt in self._nodes.iteritems():
            for nbr in nt.nbrs:
                if nbr not in self._nodes:
                    # Missing node
                    msg = ('node ' + str(n) + ' has a neighbor (' +
                           str(nbr) + ') that is not a node in the graph')
                    raise UserWarning(msg)
                elif n not in self._nodes[nbr].nbrs:
                    # Missing edge
                    msg = ('edge from ' + str(n) + ' to ' + 
                           str(nbr) + ', but not from ' + 
                           str(nbr) + ' to ' + str(n))
                    raise UserWarning(msg)
                elif self._nodes[n].nbrs[nbr] != self._nodes[nbr].nbrs[n]:
                    # Mismatched attribute
                    msg = ('edge attributes for edge (' + str(n) +
                           ', ' + str(nbr) + ') are mismatched: ' +
                           str(self._nodes[n].nbrs[nbr]) + ' and ' +
                           str(self._nodes[nbr].nbrs[n]))
                    raise UserWarning(msg)

