
import numpy as np
import networkx as nx
from networkx.generators.small import krackhardt_kite_graph

import matplotlib.pyplot as plt

def DFS_nodes(graph, node, visited=[]):
    visited.append(node)
    for neighbor in graph.neighbors(node):
        if not neighbor in visited:
            DFS_nodes(graph, neighbor, visited)            
    return visited
    
def trim_degrees(G, degree=1):
    G2 = G.copy()
    deg = nx.degree(G2)
    for n in G2.nodes():
        if deg[n] <= degree:
            G2.remove_node(n)
    return G2


if __name__ == '__main__':
    
    G = krackhardt_kite_graph()
    
    plt.figure()
    nx.draw(G, with_labels=True)
    
    edges = nx.traversal.dfs_edges(G)
    print "DFS edges: ", list(edges)
    
    edges = nx.traversal.bfs_edges(G)
    print "BFS edges: ", list(edges)
    
    path = nx.algorithms.shortest_path(G, 0, 9)
    print "Shortest Path: ", path
    
    path = nx.algorithms.dijkstra_path(G, 0, 9)
    print "Dijkstra Path: ", path
    
    deg = nx.degree(G)
    print "max degree: ", max(deg.values())
    
    sub = list(nx.connected_component_subgraphs(G))
    x = [len(c) for c in sub]
    
    cliques = list(nx.find_cliques(G))
    print "num cliques: ", len(cliques)
    
    