# Center-Based Frequencey Clustering (CBFC)

The formulation of Center-Based Frequency Clustering (CBFC) was motivated in large part by the need for a method to determine the next procedurally generated environment in a dynamic driving simulator. Via the problem specification, the choice of next environment, or map, was to be driven by the user's performance in a series of "testing parameters" experienced in previous maps and the relatedness of the parameters. To acheive this, the following steps were taken to generate an analogous graph:
* The number of nodes that correspond to a particular testing parameter is equal to that parameter's score.
* Edges are assigned incident to nodes/parameters that occur in the same map.
* Edges are given a weight with an anti-correlation to the number of maps shared by incident nodes

The CBFC algorithm was then designed to isolate the nodes corresponding to the testing parameters the user would most benefit from practicing by taking into account the current score for each parameter (judging node frequency) and the likelyhood that testing one high-scoring parameter would cause the testing of another high-scoring parameter by means of occurence in the same map (judging how embeded the parameter's clique was in the graph using the graph-theoretic center).

The psuedocode for the algorithm is pictured here in the poster used for publication:

![DrivingSimulator USF Poster](https://user-images.githubusercontent.com/78307866/209899836-d97f961a-1637-4709-85e1-77faf621267d.jpg)
[MIT licensed](./LICENSE) © 2022 [Malik Zekri](https://github.com/TheShadowTiki)
