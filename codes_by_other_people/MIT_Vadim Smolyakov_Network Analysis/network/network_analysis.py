import networkx as nx
import numpy as np
import pandas as pd

from collections import Counter
from itertools import combinations

import matplotlib.pyplot as plt

def load_seventh_grader_network():
    
    #read the edge list
    edges = pd.read_csv('./data/moreno_seventh/out.moreno_seventh_seventh', skiprows=2, sep = " ", header=None)
    edges.columns = ['student1', 'student2', 'count']
    
    #read node metadata
    meta = pd.read_csv('./data/moreno_seventh/ent.moreno_seventh_seventh.student.gender', header=None)
    meta.index += 1
    meta.columns = ['gender']
    
    #construct the graph
    G = nx.DiGraph()
    for row in edges.iterrows():
        G.add_edge(row[1]['student1'], row[1]['student2'], count=row[1]['count'])
        
    #add meta data
    for i in G.nodes():
        G.node[i]['gender'] = meta.ix[i]['gender']
    
    return G
    
def get_triangles(G, node):

    triangle_nodes = set()
    triangle_nodes.add(node)
    
    for nbr1, nbr2 in combinations(G.neighbors(node), 2):
        if G.has_edge(nbr1, nbr2):
            triangle_nodes.add(nbr1)
            triangle_nodes.add(nbr2)
    
    return triangle_nodes


if __name__ == "__main__":
    
    G = load_seventh_grader_network()
    
    plt.figure()
    nx.draw(G)    
        
    print "number of nodes: ", len(G.nodes())
    print "number of edges: ", len(G.edges())
    
    #graph counts        
    mf_counts = Counter([d['gender'] for n, d in G.nodes(data=True)])
    fv_counts = [d['count'] for _,_,d in G.edges(data=True)]
    maxcount = max(fv_counts)    
    print mf_counts
    print "max favorite count: ", maxcount
    
    #adjacency matrix
    adj_matrix = nx.to_numpy_matrix(G)    
    plt.figure()
    plt.pcolor(np.array(adj_matrix),cmap='Greys')
    plt.axes().set_aspect('equal')
    plt.xlim(min(G.nodes()), max(G.nodes()))
    plt.ylim(min(G.nodes()), max(G.nodes()))
    plt.title('Adjacency Matrix')
    plt.show()
    
    #hubs and centrality
    hubs = sorted([(n, G.neighbors(n)) for n in G.nodes()], key=lambda x: len(x[1]), reverse=True)
    neighbors = [len(G.neighbors(node)) for node in G.nodes()]    
    in_centrality = nx.in_degree_centrality(G)
    out_centrality = nx.out_degree_centrality(G)    
    print "top hub node: ", hubs[0][0]

    #page rank    
    ranking = nx.pagerank(G, alpha=0.9)    
    plt.figure()
    plt.bar(ranking.keys(), ranking.values())
    plt.xlabel('nodes')
    plt.ylabel('rank')
    plt.title('Page Rank')
    plt.show()
    
    #triangles sub-graph
    get_triangles(G,1)
    plt.figure()
    nx.draw(G.subgraph(get_triangles(G,1)))
    
    #erdos-renyi graph
    erG = nx.erdos_renyi_graph(n=len(G.nodes()),p=nx.density(G))
    plt.figure()
    nx.draw(erG)

    #degree centralities
    erG_deg_centralities = list(nx.degree_centrality(erG).values())
    plt.figure()
    plt.hist(erG_deg_centralities)
    plt.xlabel('centrality')
    plt.title('Degree Centrality')
    
    
    
    
    
    
    
    