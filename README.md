# Center-Based Frequencey Clustering (CBFC)

The formulation of Center-Based Frequency Clustering (CBFC) was motivated in large part by the need for a method to determine the next procedurally generated environment in a dynamic driving simulator. Via the problem specification, the choice of next environment, or map, was to be driven by the user's performance in a series of "testing parameters" experienced in previous maps and the relatedness of the parameters. To achieve this, the following steps were taken to generate an analogous graph:
* The number of nodes that correspond to a particular testing parameter is equal to that parameter's score.
* Edges are assigned incident to nodes/parameters that occur in the same map.
* Edges are given a weight with an anti-correlation to the number of maps shared by incident nodes

The CBFC algorithm was then designed to consolidate the nodes corresponding to the testing parameters the user would most benefit from practicing by taking into account the current score for each parameter (judging node frequency) and the likelihood that testing one high-scoring parameter would cause the testing of another high-scoring parameter by means of occurence in the same map (judging how embedded the parameter's clique was in the graph using the graph-theoretic center).

The pseudocode for the algorithm is pictured here in the poster used for publication:

![DrivingSimulator USF Poster](https://user-images.githubusercontent.com/78307866/209899836-d97f961a-1637-4709-85e1-77faf621267d.jpg)

# Contents
* graph.py
  * Node class: Locally designed node class for use in graph class.
  * Graph class: Locally designed graph class.
    * Specialized Methods:
      * Dijkstra's Algorithm
      * CBFC
      * View (using networkx and matplotlib.pyplot)
  * Required modules:
      * numpy
      * matplotlib.pyplot
      * networkx
      * itertools.chain
* cbfc_implementation.py
  * Implementation of CBFC algorithm within the driving simulator context described above.
  * Required modules:
    * graph (local)
    * itertools.chain
    * random

# Use Examples
Graphs can be created from a list of Node objects or by specifying the number of nodes the graph should contain.

![image](https://user-images.githubusercontent.com/78307866/209971873-ffbb69d0-5e05-4cab-8531-528cc18c45d3.png)

![image](https://user-images.githubusercontent.com/78307866/209971897-aa628ba0-3c37-44b4-b967-327b0cdf7816.png)

To tinker with CBFC in its intended application, modify the "scores" and "maps" collections in the cbfc_implementation.py file.

![image](https://user-images.githubusercontent.com/78307866/209973215-e074e990-e532-49a8-a641-d16af3bbed76.png)

[MIT licensed](./LICENSE) © 2022 [Malik Zekri](https://github.com/TheShadowTiki)
