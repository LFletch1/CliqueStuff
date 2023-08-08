import networkx as nx
import matplotlib.pyplot as plt
from pruning_test import get_DODGr
from itertools import combinations

def get_largest_clique(G):
    largest_clique = []
    for clique in nx.find_cliques(G):
        if len(clique) > len(largest_clique):
            largest_clique = clique
    return largest_clique

def large_clique_heuristic_test(DODGr, G, largest_clique, k):
    '''
        k - size of cliques being searched for.
    '''
    L_clique_dict = {n:True for n in largest_clique}
        
    total_combos = 0
    total_nodes = 0
    num_of_colorings = 0
    for edge in DODGr.edges():
        num_of_colorings = len(DODGr[edge[0]][edge[1]]["colorings"])
        break
    combos_pruned = 0
    wedge_checks = 0
    wedge_checks_shortcutted: 0
    for u in DODGr.nodes():
        sorted_neighbors = [n[0] for n in sorted(G.degree(DODGr.neighbors(u)), key = lambda x: x[1])]
        for combo in combinations(sorted_neighbors, k-1):
            total_combos += 1
            wedge_checks += k-2
            all_in_L_clique = True
            nodes_in_L_clique = 0
            for node in combo:
                if node in L_clique_dict:
                    nodes_in_L_clique += 1
            if nodes_in_L_clique >= 2:
                wedge_checks_shortcutted += 1
                # if not node in L_clique_dict:
                #     all_in_L_clique = False
                #     break
            if all_in_L_clique:
                combos_pruned += 1 
    return wedge_checks_shortcutted, combos_pruned, total_combos



def main(): 
    filenames = [("musae_PTBR_edges.csv", ","),
                 ("musae_RU_edges.csv", ","),
                 ("musae_ENGB_edges.csv", ","),
                 ("musae_ES_edges.csv", ","),
                 ("musae_FR_edges.csv", ","),
                 ("musae_FR_edges.csv", ","),
                 ("Email-Enron.txt", "\t"),
                 ("musae_DE_edges.csv", ",")]
    dir_name = "graphs/"
    for filename in filenames:
        graph_name = filename[0].split(".")[0]
        # print("-" * 80)
        G = nx.read_edgelist(dir_name + filename[0], delimiter=filename[1], nodetype=int)
        DODGr = get_DODGr(G)
        largest_clique = get_largest_clique(G)
        print(f'Size of largest clique of {filename[0]}: {len(largest_clique)}')
        k = 6
        combos_pruned, total_combos = large_clique_heuristic_test(DODGr, G, largest_clique, k)
        print(f'Percentage of {k-1} combos pruned: {(combos_pruned / total_combos) * 100}')

if __name__ == "__main__":
    main()
