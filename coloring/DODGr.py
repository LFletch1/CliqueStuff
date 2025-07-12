import networkx as nx

def get_DODGr(G):
    '''Given an undirected graph return the Degree Ordered Directed Graph (DODGr)'''
    DODGr = nx.DiGraph()
    for edge in G.edges():
        # print(edge)
        if edge[0] == edge[1]:
            continue
        elif G.degree[edge[0]] > G.degree[edge[1]]:
            DODGr.add_edge(edge[1], edge[0], colorings=[], weight=0) # Edge from lesser degree node to greater degree node
        elif G.degree[edge[0]] < G.degree[edge[1]]:
            DODGr.add_edge(edge[0], edge[1], colorings=[], weight=0) # Edge from lesser degree node to greater degree node
        else: # Edges are equal, tie break based on node label
            if edge[0] < edge[1]:
                DODGr.add_edge(edge[0], edge[1], colorings=[], weight=0)
            else:
                DODGr.add_edge(edge[1], edge[0], colorings=[], weight=0)
    return DODGr


def get_DODGr_in_degree_order(DODGr):
    return sorted(DODGr, key=DODGr.in_degree) # Sorted by least in degree to greatest in degree


def get_DODGr_order(DODGr):
    order = []
    tmp_graph = DODGr.copy()
    while tmp_graph.number_of_nodes() > 0:
        tmp_nodes = [n for n in tmp_graph.nodes()]
        for n in tmp_nodes:
            if tmp_graph.in_degree(n) == 0:
                order.append(n)
                tmp_graph.remove_node(n)
    return order