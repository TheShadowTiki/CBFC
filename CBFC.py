import matplotlib.pyplot as plt
import igraph
from igraph import plot,layout,Graph,summary
from itertools import combinations
from collections import Counter, OrderedDict
import random

def get_params(num_params):
    test_params = []
    for param in range(num_params):
        test_params.append(f't{param}')
    return test_params
def get_scores(test_params):
    scores = []
    for param in test_params:
        scores.append(int(input(f'Enter score for {param}: ')))
    return scores
def get_clusters(num_clus, test_params):
    clusters = []
    for clus in range(num_clus):
        c = input(f'Enter params for c{clus}: ').split(' ')
        for t in range(len(c)):
            c[t] = test_params[int(c[t])]
        clusters.append(c)
    return clusters
def get_edges(clusters):
    edges = []
    for clus in clusters:
        for combo in list(combinations(clus, 2)):
            edges.append(combo)
    return list(OrderedDict.fromkeys(edges))
def get_weight_test(test_params, scores):
    b = dict(Counter(test_params))
    for i in range(len(test_params)):
        b[test_params[i]] = scores[i]
    temp = []
    tot = []
    for i in b:
        temp.append(i)
        temp *= b[i]
        tot.append(temp)
        temp=[]
    t = [tot[-1]]
    for i in range(len(tot)-1):
        t.append(tot[len(tot)-(i+2)] + t[-1])
    return t[-1]
def get_edge_weight(edge, clusters):
    weight = 0
    edge = list(edge)
    for clus in clusters:
        if any(clus[idx : idx + len(edge)] == edge for idx in range(len(clus) - len(edge) + 1)) or (edge[0] == edge[1] and edge[0] in clus):
            weight += 1
    weight = len(clusters) - weight
    return weight

pnum = 4
cnum = 3
test = get_params(pnum)
score_ls = get_scores(test)
clust_ls = get_clusters(cnum, test)
    
gr = Graph(sum(score_ls))
gr.vs['name'] = get_weight_test(test, score_ls)
edge_ls = get_edges(clust_ls)
for node1 in gr.vs():
    for node2 in gr.vs():
        if (node1['name'], node2['name']) in edge_ls or \
            (node1['name'] == node2['name'] and node1 != node2 and (node2.index, node1.index) not in gr.get_edgelist()):
            gr.add_edge(node1, node2, width = get_edge_weight((node1['name'], node2['name']), clust_ls))
            gr.es[gr.get_eid(node1.index, node2.index)]['weight'] = get_edge_weight((node1['name'], node2['name']), clust_ls)
            
def clustering(g):
    ecc = {}
    for node1 in g.vs():
        dis = []
        for node2 in g.vs():
            l = g.get_shortest_paths(node1, node2, g.es['weight'])
            for i in range(len(l[0])-1):
                l.append(g.es[g.get_eid(l[0][i], l[0][i+1])]['weight'])
            l = [x for x in l if not isinstance(x, list)]
            dis.append(sum(l))
        ecc[node1.index] = max(dis)

    center = [x.index for x in g.vs() if ecc[x.index] == min(ecc.values())]
    center_deg = sum([g.degree(x) for x in center])
    params_to_gen = []
    for param in test:
        params_to_gen.append(sum([g.degree(x.index) for x in g.vs() if x['name'] == param]))
        params_to_gen[-1] = 'None' if params_to_gen[-1] < center_deg else param
    params_to_gen = [x for x in params_to_gen if x != 'None'] 

    while [x for x in list(combinations(params_to_gen, 2)) if (x not in edge_ls and x[0] != x[1])] != []:
        for pairs in list(combinations(params_to_gen, 2)):
            if pairs not in edge_ls and pairs[0] != pairs[1]:
                dif = sum([g.degree(x.index) for x in g.vs() if x['name'] == pairs[0]]) - sum([g.degree(x.index) for x in g.vs() if x['name'] == pairs[1]])
                out = pairs[0] if (dif < 0 or pairs[1] in g.vs[center]['name']) else pairs[1]
                out = random.choice([pairs[0], pairs[1]]) if dif == 0 else out
                params_to_gen = [x for x in params_to_gen if x is not out] 

    chunk = random.choice([x for x in clust_ls if len(params_to_gen) == len([e for e in params_to_gen if e in x])])
        
    ug = g.subgraph([x.index for x in g.vs() if x['name'] not in chunk])
    ug.add_vertices(1)
    ug.vs[-1]['name'] = f'{chunk}'
    print(chunk)
    return ug
graphs =[gr]
i = 0.5

for l in range(1):
    graphs.append(clustering(gr))
    gr = graphs[-1]
    i += 0.5

lay1 = gr.layout('kk')
fig, (ax1,ax2) = plt.subplots(1,2, figsize=(12,8))

for gra in graphs:
    if gra == graphs[0]:
        plot(gra, target=ax1, layout=gra.layout('drl'), vertex_label=gra.vs['name'], edge_width=0.5, vertex_label_size=20)     
    elif gra == graphs[1]:
        plot(gra, target=ax2, layout=gra.layout('circle'), vertex_label=gra.vs['name'], edge_width=0.5, vertex_label_size=20)    
ax1.axis('off')
ax2.axis('off')  