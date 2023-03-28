import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt

def get_DODGr(G):
    '''Given an undirected graph return the Degree Ordered Directed Graph (DODGr)'''
    DODGr = nx.DiGraph()
    for edge in G.edges():
        # print(edge)
        if G.degree[edge[0]] > G.degree[edge[1]]:
            DODGr.add_edge(edge[1], edge[0], colorings=[]) # Edge from lesser degree node to greater degree node
        elif G.degree[edge[0]] < G.degree[edge[1]]:
            DODGr.add_edge(edge[0], edge[1], colorings=[]) # Edge from lesser degree node to greater degree node
        else: # Edges are equal, tie break based on node label
            if edge[0] > edge[1]:
                DODGr.add_edge(edge[0], edge[1], colorings=[])
            else:
                DODGr.add_edge(edge[1], edge[0], colorings=[])
    return DODGr

def color_DODGr(G, DODGr, c):
    '''
        Color DODGr with smallest first strategy and for each coloring after that use a random coloring.
    ''' 
    for i in range(c+1): # number of random colorings
        if i == 0:
            coloring = nx.greedy_color(G, strategy=strategy_smallest_first) # Equivalent to DODGr Coloring
        else:
            coloring = nx.greedy_color(G, strategy='random_sequential')
        for u in DODGr.nodes():
            for v in DODGr.neighbors(u):
                colorings = DODGr[u][v]["colorings"]
                colorings.append(coloring[v])
                DODGr[u][v]["colorings"] = colorings
                if coloring[u] == coloring[v]:
                    raise Exception("Coloring is improper")           
                

def colors_heuristic_test(DODGr, G, k):
    '''
        k - size of cliques being listed.
    '''
    total_combos = 0
    total_combos_pruned = 0
    total_nodes = 0
    num_of_colorings = 0
    for edge in DODGr.edges():
        num_of_colorings = len(DODGr[edge[0]][edge[1]]["colorings"])
        break
    combos_pruned_by_number_of_colors = [0] * (num_of_colorings + 1)
    for u in DODGr.nodes():
        # total_nodes += 1
        # if (total_nodes % 100) == 0:
        #     print("Nodes Processed: ", total_nodes)
        #     print("Total Combos: ", total_combos)
        sorted_neighbors = [n[0] for n in sorted(G.degree(DODGr.neighbors(u)), key = lambda x: x[1])]
        neighbor_colors = []
        for col in range(num_of_colorings): # Number of colors, hard coded for now
            color_round = []
            for v in sorted_neighbors:
                color_round.append(DODGr[u][v]["colorings"][col])
            neighbor_colors.append(color_round)
        new_sorted_neigh = [i for i in range(len(sorted_neighbors))]
        for combo in combinations(new_sorted_neigh, k-1):
            total_combos += 1
            # color_prune = False
            for col in range(num_of_colorings): # Number of colors, hard coded for now
                col_list = [neighbor_colors[col][c] for c in combo]
                if len(col_list) != len(set(col_list)):
                    # color_prune = True
                    combos_pruned_by_number_of_colors[col+1] += 1
                    break
            # if color_prune:
            #     total_combos_pruned += 1
    return combos_pruned_by_number_of_colors
    print(f"Total combinations of {k-1} to be checked: {total_combos}")
    print(f"Total combinations pruned from {num_of_colorings} colorings: {total_combos_pruned}")


def strategy_smallest_first(G, colors):
    return sorted(G, key=G.degree) # sorts least to greatest

def strategy_out_degree(DODGr, colors):
    return sorted(DODGr, key=DODGr.out_degree, reverse=True) # Greatest to least

def prefix_sum(nums_list):
    new_list = [0] * len(nums_list)
    new_list[0] = nums_list[0]
    nums_list
    for i in range(1,len(nums_list)):
        new_list[i] = new_list[i-1] + nums_list[i]
    print(nums_list)
    print(new_list)


def main():
    # filenames = [("facebook_combined.txt", " ")]
    #             ("Email-Enron.txt", "\t"))
                # ("musae_facebook_edges.csv", ","))
                # ("musae_DE_edges.csv", ","),
    filenames = [("musae_PTBR_edges.csv", ","),("musae_RU_edges.csv", ",")] #,
    # filenames = [("musae_RU_edges.csv", ",")] #,
    # filenames = [("musae_ES_edges.csv", ",")] #,
                # ("musae_ENGB_edges.csv", ","),
                # ("musae_ES_edges.csv", ","),
                # ("musae_FR_edges.csv", ","),
                # ("musae_RU_edges.csv", ","),
    # for filename_delim in filenames:
    #     compare_colorings(filename_delim[0], filename_delim[1])
    clique_size = 4
    colorings_to_test = 5
    for filename in filenames:
        for k in range(3,clique_size+1):
            G = nx.read_edgelist(filename[0], delimiter=filename[1], nodetype=int)
            DODGr = get_DODGr(G)
            # max_degree_G = max([v[1] for v in G.degree()])
            # max_degree_DODGr = max([v[1] for v in DODGr.out_degree()])
            # print(sorted(DODGr.out_degree, key=lambda x: x[1], reverse=False)[-10:])
            DODGr = get_DODGr(G)
            print("-" * 80)
            print(f"Clique Size: {k}") 
            color_DODGr(G, DODGr, colorings_to_test)
            prune_by_color = colors_heuristic_test(DODGr, G, k)
            # print(prune_by_color)
            prefix_sum(prune_by_color)

if __name__ == "__main__":
    main()