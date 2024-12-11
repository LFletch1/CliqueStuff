import networkx as nx

def get_DODGr(G):
    '''Given an undirected graph return the Degree Ordered Directed Graph (DODGr)'''
    DODGr = nx.DiGraph()
    for edge in G.edges():
        # print(edge)
        if G.degree[edge[0]] > G.degree[edge[1]]:
            DODGr.add_edge(edge[1], edge[0], colorings=[], weight=0) # Edge from lesser degree node to greater degree node
        elif G.degree[edge[0]] < G.degree[edge[1]]:
            DODGr.add_edge(edge[0], edge[1], colorings=[], weight=0) # Edge from lesser degree node to greater degree node
        else: # Edges are equal, tie break based on node label
            if edge[0] < edge[1]:
                DODGr.add_edge(edge[0], edge[1], colorings=[], weight=0)
            else:
                DODGr.add_edge(edge[1], edge[0], colorings=[], weight=0)
    return DODGr

def get_DODGr_out_degree_order(DODGr):
    return sorted(DODGr, key=DODGr.out_degree, reverse=True) # Greatest to least