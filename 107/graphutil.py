"""
This module provides a number of useful functions for viewing graphs
and plotting data.
"""

import matplotlib.pyplot as plt
import pylab
import networkx
import types

def draw(g, title=None):
    """
    Draw the graph g on the screen.

    g is assumed to be a dictionary of sets where the dictionary keys
    are the nodes in the graph and the dictionary values are the set
    of neighboring nodes.

    The optional title argument enables you to set the window title.
    """
    fig = _fig(g)
    if title:
        fig.canvas.set_window_title(title)
    fig.show()

def save(g, filename):
    """
    Save a picture of the graph g to the file named filename.  The
    picture will be saved as a PNG file.

    g is assumed to be a dictionary of sets where the dictionary keys
    are the nodes in the graph and the dictionary values are the set
    of neighboring nodes.
    """
    fig = _fig(g)
    fig.savefig(filename)

def show():
    """
    Do not use this function unless you have trouble with figures.

    It may be necessary to call this function after drawing/plotting
    all figures.  If so, it should only be called once at the end.
    """
    plt.show()

def read_graph(filename):
    """
    Read a graph from a file.  The file is assumed to hold a graph
    that was written via the write_graph function.
    """
    with open(filename) as f:
        g = eval(f.read())
    return g

def write_graph(g, filename):
    """
    Write a graph to a file.  The file will be in a format that can be
    read by the read_graph function.
    """
    with open(filename, 'w') as f:
        f.write(repr(g))

def plot_dist(data, title, xlabel, ylabel, filename=None):
    """
    Plot the distribution provided in data.

    The data argument must be a dictionary, which will be plotted with
    the keys on the x axis and the values on the y axis.

    title, xlabel, and ylabel will be used as the title and axis
    labels of the plot.

    If an optional filename is provided, the plot will be saved to
    that file (in png format).
    """
    ### Check that the data is a dictionary
    if not isinstance(data, types.DictType):
        msg = "data must be a dictionary, not {0}".format(type(data).__name__)
        raise TypeError(msg)

    ### Create a new figure
    fig = pylab.figure()

    ### Plot the data
    _plot_dict(data)
    
    ### Label the plot
    pylab.title(title)
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)

    ### Show the plot
    fig.show()

    ### Save to file
    if filename:
        pylab.savefig(filename)

def plot_lines(data, title, xlabel, ylabel, labels=None, filename=None):
    """
    Plot a line graph with the provided data.

    The data argument must be a list of dictionaries, each of which
    will be plotted as a line with the keys on the x axis and the
    values on the y axis.

    title, xlabel, and ylabel will be used as the title and axis
    labels of the plot.

    If an optional list of labels is provided, a legend will be drawn
    with the given labels.  The label list must correspond to the data
    list.

    If an optional filename is provided, the plot will be saved to
    that file (in png format).
    """
    ### Check that the data is a list
    if not isinstance(data, types.ListType):
        msg = "data must be a list, not {0}".format(type(data).__name__)
        raise TypeError(msg)

    ### Create a new figure
    fig = pylab.figure()

    ### Plot the data
    if labels:
        mylabels = labels[:]
        for i in range(len(data)-len(labels)):
            mylabels.append("")
        for d, l in zip(data, mylabels):
            _plot_dict_line(d, l)
        # Add legend
        pylab.legend(loc='best')
    else:
        for d in data:
            _plot_dict_line(d)

    ### Set the lower y limit to 0
    pylab.ylim(ymin=0)

    ### Label the plot
    pylab.title(title)
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)

    ### Show the plot
    fig.show()

    ### Save to file
    if filename:
        pylab.savefig(filename)

def _fig(g):
    """
    Create a figure from the graph g.  Returns the figure object.

    g is assumed to be a dictionary of sets where the dictionary keys
    are the nodes in the graph and the dictionary values are the set
    of neighboring nodes.
    """
    nxg = networkx.Graph(g)
    fig = plt.figure()
    networkx.draw(nxg)
    return fig

def _dict2lists(data):
    """
    Convert a dictionary into a list of keys and values, sorted by
    key.  Returns a tuple of two lists.
    """
    xvals = data.keys()
    xvals.sort()
    yvals = []
    for x in xvals:
        yvals.append(data[x])
    return xvals, yvals

def _plot_dict_line(d, label=None):
    """
    Plot data in the dictionary d on the current plot. 
    """
    xvals, yvals = _dict2lists(d)
    if label:
        pylab.plot(xvals, yvals, label=label)
    else:
        pylab.plot(xvals, yvals)

def _plot_dict(d, label=None):
    """
    Plot data in the dictionary d on the current plot. 
    """
    xvals, yvals = _dict2lists(d)
    if label:
        pylab.bar(xvals, yvals, align='center', label=label)
        pylab.xlim([-1, max(xvals)+1])
    else:
        pylab.bar(xvals, yvals, align='center')
        pylab.xlim([-1, max(xvals)+1])
    
