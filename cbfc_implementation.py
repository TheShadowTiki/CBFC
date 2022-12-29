# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 23:28:29 2022

@author: mikoz
"""

from graph import *
from itertools import chain
import random

"""
The formulation of Center-Based Frequency Clustering (CBFC) was motivated in
large part by the need for a method to determine the next procedurally generated
environment in a dynamic driving simulator. Via the problem specification, the
choice of next environment, or map, was to be driven by the user's performance
in a series of "testing parameters" experienced in previous maps and the relatedness
of the parameters. To acheive this, the following steps were taken to generate
an analogous graph:
    
    * The number of nodes that correspond to a particular testing parameter
      is equal to that parameter's score.
      
    * Edges are assigned incident to nodes/parameters that occur in the same map.
    
    * Edges are given a weight with an anti-correlation to the number of maps
      shared by incident nodes
"""

if __name__ == '__main__':
    scores = {'t0': 4, 't1': 2, 't2': 6, 't3': 5}
    maps = [('t0', 't1'), ('t1', 't2'), ('t1', 't3')]
    
    g = Graph(list(chain(*[[Node(param) for i in range(score)] for param, score in scores.items()])))
    for n1 in g.nodes:
        for n2 in g.nodes:
            if n2 not in n1.neighbors and n1 != n2:
                params = [n1.label] if n1.label == n2.label else [n1.label, n2.label]
                embed = [all([p in m for p in params]) for m in maps]
                if any(embed):
                    g.add_edge(n1, n2, len(maps) - sum(embed) + 1)
    g.view(node_size=200, forced_layout=nx.kamada_kawai_layout)
    cluster = g.cbfc()
    next_map = random.choice([m for m in maps if all([c.label in m for c in cluster])])
    new_graph = Graph(g.nodes[:])
    new_graph.add_node(Node(str(next_map)))
    for node in new_graph.nodes[:]:
        if node.label in next_map: new_graph.remove_node(node)
    new_graph.view(node_size=200, forced_layout=nx.circular_layout)
