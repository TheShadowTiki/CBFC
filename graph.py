# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 21:55:03 2022

@author: mikoz
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from itertools import chain
import random

class Node():
    """Node for use in a graph or network.
    
    Parameters
    ----------
    label : str, required
        Label or name of the Node. Appears as repesentation
        in printed collections of Nodes via override of __repr__().
    neighbors : dict, optional
        Dict of {Node : edge_weight} pairs to be added as neighbors, establishing 
        edges when implemented in a graph. The default is {}.
    attributes : dict, optional
        A Node can be initialized with attributes in this dict through
        {attr : value} pairs. These attributes are stored directly to __dict__,
        allowing access through standard python dot notation. The default is {}.
    **kwargs : additional keyword arguments
        Attributes can also be initialized through keyword arguments and
        are stored in the same way as those passed through the attributes
        parameter.
    
    Atributes
    ---------
    label : str
        Label or name of the Node. Appears as repesentation
        in printed collections of Nodes via overide of __repr__().
    neighbors : dict
        Dict of {Node : edge_weight} pairs to be added as neighbors, establishing 
        edges when implemented in a graph.
    """
     
    def __init__(self, label, neighbors={}, attributes={}, **kwargs):
        self.label = label
        self.neighbors = {} if neighbors == {} else neighbors
        for attr in attributes: self[attr] = attributes[attr]
        for attr in kwargs: self[attr] = kwargs[attr]
    
    def add_neighbor(self, node, weight=1):
        self.neighbors[node] = weight
        node.neighbors[self] = weight
        
    def remove_neighbor(self, node):
        try: self.neighbors.pop(node)
        except: pass
        try: node.neighbors.pop(self)
        except: pass
        
    def degree(self):
        return(len(self.neighbors))
    
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __setitem__(self, key, value):
        self.__dict__[key] = value
    
    def __delitem__(self, key):
        del self.__dict__[key]
        
    def __repr__(self):
        return self.label
    
    def __str__(self):
        return str(self.__dict__)

class Graph():
    """Graph class for graph/network theoretic applications, particularly as an
    example class for demonstration of Center-Based Frequency Clustering (CBFC).
    
    Parameters
    ----------
    nodes : list, required
        List of Nodes to compose the graph.
    
    Atributes
    ---------
    nodes : list
        List of Nodes which the graph is composed of.
    edges : dict
        Dict of {frozenset((node1, node2)) : edge_weight} pairs representing edges
        between pairs of neighboring Nodes.
    """
    
    def __init__(self, nodes):
        self.nodes = nodes
        self.edges = self.get_edges()
        self.adj = self.get_adj_matrix()
    
    def get_edges(self):
        edges = {}
        for node in self.nodes:
            edges.update({frozenset((node, n)): w for n, w in node.neighbors.items() if (n, node) not in edges.keys() and n in self.nodes})
        return edges
    
    def get_adj_matrix(self):
        rows = [[self.edges[frozenset((n1, n2))] if frozenset((n1, n2)) in self.edges.keys() else 0 for n2 in self.nodes] for n1 in self.nodes]
        return np.array(rows)
    
    def update_weight(self, node1, node2, weight):
        edge = (node1, node2) if isinstance(node1, Node) and isinstance(node2, Node) else (self.nodes[node1], self.nodes[node2])
        edge[0].neighbors[edge[1]] = weight
        edge[1].neighbors[edge[0]] = weight
        self.edges = self.get_edges()
        self.adj = self.get_adj_matrix()
        
    def add_node(self, node):
        self.nodes.append(node)
        self.edges = self.get_edges()
        self.adj = self.get_adj_matrix()
    
    def remove_node(self, node, delete=False):
        self.nodes.remove(node)
        for n in self.nodes:
            node.remove_neighbor(n)
        self.edges = self.get_edges()
        self.adj = self.get_adj_matrix()
        if delete: del node
    
    def add_edge(self, node1, node2, weight=1):
        edge = (node1, node2) if isinstance(node1, Node) and isinstance(node2, Node) else (self.nodes[node1], self.nodes[node2])
        edge[0].add_neighbor(edge[1], weight)
        edge[1].add_neighbor(edge[0], weight)
        self.edges = self.get_edges()
        self.adj = self.get_adj_matrix()
    
    def remove_edge(self, node1, node2):
        del self.edges[frozenset((node1, node2))]
        node1.remove_neighbor(node2)
        self.adj = self.get_adj_matrix()
    
    @staticmethod
    def create(num_nodes, label='n'):
        nodes = [Node(f'{label}{num}') for num in range(num_nodes)]
        return Graph(nodes)
    
    def dijkstra(self, node):
        visited = []
        to_visit = [node]
        paths = {k : [np.sum(self.adj) + 1, []] for k in self.nodes if k != node}
        paths[node] = [0, []]
        while set(visited) != set(self.nodes):
            cur = to_visit.pop(0)
            for n in [n for n in cur.neighbors if n not in visited]:
                new_val = paths[cur][0] + self.edges[frozenset((cur, n))]
                if new_val < paths[n][0]:
                    paths[n][0] = new_val
                    paths[n][1] = paths[cur][1] + [(cur, n)]
                to_visit.append(n)
            to_visit.sort(key=lambda i : paths[i][0])
            visited.append(cur)
        return paths
    
    def cbfc(self, cluster_attr='label'):
        for n in self.nodes:
            n['dijkstra'] = self.dijkstra(n)
            n['ecc'] = max([i[0] for i in n.dijkstra.values()])
        center = [n for n in self.nodes if n.ecc == min(self.nodes, key=lambda i : i.ecc).ecc]
        cluster = center + [n for n in self.nodes if sum([_n.degree() for _n in self.nodes if _n[cluster_attr] == n[cluster_attr]]) > sum([_n.degree() for _n in center])]
        disconnected = list(chain(*[[(n, _n) for _n in cluster if frozenset((n, _n)) not in self.edges.keys()] for n in cluster]))
        out = [min(e, key=lambda i : sum([n.degree() for n in self.nodes if n[cluster_attr] == i[cluster_attr]])) for e in disconnected]
        cluster = [n for n in cluster if n not in out]
        return cluster
        
    def view(self, figsize=(5,5), forced_layout=None, **kwargs):
        edges = [(self.nodes.index(n1), self.nodes.index(n2), w) for (n1, n2), w in self.edges.items()]
        gr = nx.Graph()
        for n in range(len(self.nodes)):
            gr.add_node(n)
        gr.add_weighted_edges_from(edges)
        plt.rcParams["figure.figsize"] = figsize
        nx.draw(gr, pos=forced_layout(gr) if forced_layout != None else None, labels={self.nodes.index(n): n.label for n in self.nodes}, with_labels=True, **kwargs)
        plt.show()