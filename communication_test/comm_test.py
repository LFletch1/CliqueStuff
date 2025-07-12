import networkx as nx
import math
from itertools import combinations
from functools import cmp_to_key

def read_graph_from_file(filename):
    G = nx.Graph()
    with open(filename, 'r') as f:
        for line in f:
            # u, v = line.strip().split('\t')
            u, v = line.strip().split(',')
            G.add_edge(int(u), int(v))
    return G

def get_DODGr(graph):
    dodgr = nx.DiGraph()
    skips = 0
    for v in graph.nodes():
        for n in graph.neighbors(v):
            if (v < n):
                if graph.degree(v) < graph.degree(n):
                    dodgr.add_edge(v,n)
                elif graph.degree(v) > graph.degree(n):
                    dodgr.add_edge(n,v)
                else:
                    if v < n:
                        dodgr.add_edge(v,n)
                    else:
                        dodgr.add_edge(n,v)

    max_degree = 0
    for v in graph.nodes():
        d = len(list(graph.neighbors(v)))
        if d > max_degree:
            max_degree = d
    print(f"Max degree in original graph: {max_degree}")

    max_degree = 0
    for v in dodgr.nodes():
        d = len(list(dodgr.neighbors(v)))
        if d > max_degree:
            max_degree = d
    print(f"Max degree in DODGr: {max_degree}")
    
    return dodgr

def intersection_approach_counts(dodgr, graph, k):

    messages = 0
    vertices_sent = 0
    cliques_found = 0

    def find_cliques(v, P_set, dodgr, graph, l, k):
        v_set = set(dodgr.neighbors(v))
        i_set = v_set.intersection(P_set)
        if len(i_set) < l:
            return 0, 0, 0
        elif l == 1:
            return len(i_set), 1, len(P_set)
        else:
            i_list = list(i_set)
            i_list = sorted(i_list, key=graph.degree)
            total_sub_cliques = 0
            total_sub_messages = 0
            total_sub_vertices_sent = 0
            for n in range(len(i_list)):
                if l != k-1:
                    total_sub_messages += 1
                    total_sub_vertices_sent += len(i_list[n+1:])
                new_P_set = set(i_list[n+1:])
                sub_cliques, sub_messages, sub_vertices_sent = find_cliques(i_list[n], new_P_set, dodgr, graph, l-1, k)
                total_sub_cliques += sub_cliques
                total_sub_messages += sub_messages
                total_sub_vertices_sent += sub_vertices_sent
            return total_sub_cliques, total_sub_messages, total_sub_vertices_sent

    cliques_found = 0
    for u in graph.nodes():
        P_set = set(graph.nodes())
        sub_cliques, sub_messages, sub_vertices_sent = find_cliques(u, P_set, dodgr, graph, k-1, k)
        cliques_found += sub_cliques
        messages += sub_messages
        vertices_sent += sub_vertices_sent 
        # cliques_found += find_cliques(u, P_set, dodgr, graph, k-1, k)
    
    print(cliques_found)
        
    return messages, vertices_sent

def wedge_checks_approach_counts(dodgr, graph, k):
    messages = 0
    vertices_sent = 0
    cliques_found = 0
    for u in graph.nodes():
        neighbors = list(dodgr.neighbors(u))
        neighbors = sorted(neighbors, key=graph.degree)
        for combo in list(combinations(neighbors, k-1)):
            messages += 1
            vertices_sent += len(combo)-1
            clique_found = True
            for i in range(len(combo)-1):
                connected = True
                v = combo[i]
                for j in range(i+1, len(combo)):
                    if combo[j] not in dodgr.neighbors(v):
                        connected = False
                        clique_found = False
                        break
                if connected and i != len(combo)-2: 
                    messages += 1
                    vertices_sent += len(combo)-i-2
                else:
                    break
            if clique_found:
                cliques_found += 1
    print(cliques_found)
    return messages, vertices_sent



# graph = read_graph_from_file("../../graphs/email-Enron.txt")
# graph = read_graph_from_file("../../graphs/cit-HepPh.txt")
# graph = read_graph_from_file("../../graphs/facebook_combined.txt")
# graph = read_graph_from_file("../../graphs/email-EuAll.txt")
graph = read_graph_from_file("../../graphs/musae_DE_edges.txt")

# graph = nx.karate_club_graph()
dodgr_graph = get_DODGr(graph)

all_combos = 0
total_gt_combos = 0
total_nodes = 0
total_gt_deg = 0
d_thresh = 50
for k in range(3,15):
    for n in dodgr_graph.nodes():
        total_nodes += 1
        d = len(list(dodgr_graph.neighbors(n)))
        all_combos += math.comb(d,k-1)
        if d > d_thresh:
            total_gt_deg += 1
            total_gt_combos += math.comb(d,k-1)
    # print(f"k: {k}, total combos: {total_c}")    
    if k == 3:
        print(f"k: {k}, % of nodes with degree greater than {d_thresh}: {(total_gt_deg / total_nodes) * 100}")
    print(f"k: {k}, % of combos from nodes with degree greater than {d_thresh}: {(total_gt_combos / all_combos) * 100}")

# for k in range(3,6):
#     messages, vertices_sent = intersection_approach_counts(dodgr_graph, graph, k)
#     print(f"k: {k}, Intersection Messages: {messages}, Vertices Sent: {vertices_sent}")
#     messages, vertices_sent = wedge_checks_approach_counts(dodgr_graph, graph, k)
#     print(f"k: {k}, Wedge Messages: {messages}, Vertices Sent: {vertices_sent}")

# cliques = list(nx.enumerate_all_cliques(graph))

# clique_counts = [0] * 6
# for clique in cliques:
#     clique_counts[len(clique)] += 1

# print(clique_counts)
