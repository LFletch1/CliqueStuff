import networkx as nx
from DODGr import *
from graph_coloring import *

def main():
                # ("musae_facebook_edges.csv", ","))
    filenames = [("musae_PTBR_edges.csv", ","),
                 ("musae_RU_edges.csv", ","),
                 ("musae_ENGB_edges.csv", ","),
                 ("musae_ES_edges.csv", ","),
                 ("musae_FR_edges.csv", ","),
                 ("musae_FR_edges.csv", ","),
                 ("Email-Enron.txt", "\t"),
                 ("musae_DE_edges.csv", ","),
                 ("facebook_combined.txt", " ")]
    # filenames = [("Email-Enron.txt", "\t")]
    clique_size = 3
    num_of_colorings = 1
    dir_name = "graphs/"
    for filename in filenames:
        graph_name = filename[0].split(".")[0]
        print("-" * 80)
        G = nx.read_edgelist(dir_name + filename[0], delimiter=filename[1], nodetype=int)
        print(f"Pruning test for {graph_name} graph") 
        DODGr = get_DODGr(G)
        max_degree_G = max([v[1] for v in G.degree()])
        max_degree_DODGr = max([v[1] for v in DODGr.out_degree()])
        print(f"Largest degree in original graph: {max_degree_G}")
        print(f"Largest degree in DODGr: {max_degree_DODGr}")
        k = 3
        print(f"Clique size k = {k}") 
        for strat in range(5):
            print("Testing Strategy:", strat)
            colorings = get_multiple_colorings(G, num_of_colorings, strat, get_DODGr_out_degree_order(DODGr), 5)
            for u in G.nodes():
                for v in G.neighbors(u):
                    if colorings[u][0] == colorings[v][0]:
                        print("BAD COLORING")
                        exit() 


if __name__ == "__main__":
    main()