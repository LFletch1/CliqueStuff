import networkx as nx
import matplotlib.pyplot as plt
from pruning_test import get_DODGr
from itertools import combinations
import math

def get_largest_clique(G):
    largest_clique = []
    for clique in nx.find_cliques(G):
        if len(clique) > len(largest_clique):
            largest_clique = clique
    return largest_clique

def count_triangles_and_weight_edges(DODGr, G):
    '''
        k - size of cliques being searched for.
    '''
    triangles = 0
    for u in DODGr.nodes():
        sorted_neighbors = [n[0] for n in sorted(G.degree(DODGr.neighbors(u)), key = lambda x: (x[1], x))]
        for combo in combinations(sorted_neighbors, 2):
            if combo[1] in DODGr.neighbors(combo[0]):
                triangles += 1
                # G[source][target]['weight'] = weight
                DODGr[u][combo[0]]['weight'] += 1
                DODGr[u][combo[1]]['weight'] += 1
    return triangles


def large_clique_heuristic_test(DODGr, G, k):
    '''
        k - size of cliques being searched for.
    '''
    total_combos = 0
    new_combos = 0
    
    for u in DODGr.nodes():
        sorted_neighbors = [n[0] for n in sorted(G.degree(DODGr.neighbors(u)), key = lambda x: x[1])]
        og_len = len(sorted_neighbors)
        if not og_len >= k-1:
            continue
        total_combos += math.factorial(og_len) / (math.factorial(k-1) * math.factorial(og_len - (k-1)))
        neighbors_with_enough_triangles = []
        for n in sorted_neighbors:
            if DODGr[u][n]['weight'] >= k-2:
                neighbors_with_enough_triangles.append(n)
        new_len = len(neighbors_with_enough_triangles)
        if not new_len >= k-1:
            continue 
        new_combos += math.factorial(new_len) / (math.factorial(k-1) * math.factorial(new_len - (k-1)))
    return total_combos-new_combos, total_combos


def main(): 
    filenames = [("musae_PTBR_edges.csv", ","),
                 ("musae_RU_edges.csv", ","),
                 ("musae_ENGB_edges.csv", ","),
                 ("musae_ES_edges.csv", ","),
                 ("musae_FR_edges.csv", ","),
                 ("Email-Enron.txt", "\t"),
                 ("musae_facebook_edges.csv", ","),
                 ("musae_DE_edges.csv", ",")]
    dir_name = "graphs/"
    for filename in filenames:
        graph_name = filename[0].split(".")[0]
        # print("-" * 80)
        G = nx.read_edgelist(dir_name + filename[0], delimiter=filename[1], nodetype=int)
        DODGr = get_DODGr(G)
        largest_clique = get_largest_clique(G)
        num_of_triangles = count_triangles_and_weight_edges(DODGr, G)
        # print(num_of_triangles)
        k = 20
        combos_pruned, total_combos = large_clique_heuristic_test(DODGr, G, k)
        print(f'Largest clique size: {len(largest_clique)}')
        print(f'Percentage of {k-1} combos pruned: {(combos_pruned / total_combos) * 100}')

if __name__ == "__main__":
    main()
