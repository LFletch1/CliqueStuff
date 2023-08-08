import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt

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
            for col in range(num_of_colorings): # Number of colors, hard coded for now
                col_list = [neighbor_colors[col][c] for c in combo]
                if len(col_list) != len(set(col_list)):
                    combos_pruned_by_number_of_colors[col+1] += 1
                    break
    return combos_pruned_by_number_of_colors, total_combos


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
    return new_list


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
    clique_size = 6
    colorings_to_test = 20
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
        continue
        for k in range(3,clique_size+1):
            DODGr = get_DODGr(G) # Have to recreate DODGr each time so that colors don't build
            print(f"Clique size k = {k}") 
            color_DODGr(G, DODGr, colorings_to_test)
            prune_by_color, total_combos = colors_heuristic_test(DODGr, G, k)
            percentage_prune = [x/total_combos for x in prune_by_color]
            percent_pruned = prefix_sum(percentage_prune)
            plt.plot([x for x in range(colorings_to_test+2)], percent_pruned, label=k)
        print("-" * 80)
        plt.legend()
        plt.title(f"Color pruning of cliques on {graph_name} graph")
        plt.xlabel("Number of colorings")
        plt.ylabel("Percentage of k-1 combos pruned")
        plt.savefig(f"charts/{graph_name}_color_pruning.png")
        plt.clf()
            

if __name__ == "__main__":
    main()