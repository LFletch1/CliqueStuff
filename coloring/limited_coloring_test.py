import networkx as nx
import math
from DODGr import *
import random as rd
from graph_coloring import *
from helper import prefix_sum
import matplotlib.pyplot as plt

# def color_DODGr(G, DODGr, c, strategy, vertex_order, arg):
def get_limited_colorings(G, c, vertex_order, limit, prob):
    # limit is the number of colors availalbe [0,limit-1]
    # Color limit-1 is reserved to be the "grey" color
    # Therefore, informative colors are in the range [0,limit-2]
    vertex_multi_colors = {u : [] for u in G.nodes()}
    for i in range(c): # number of random colorings
        coloring = {}
        for u in vertex_order:
            if (rd.random() < prob):
                coloring[u] = limit-1
            else: 
                nbr_colors = [coloring[v] for v in G[u] if v in coloring]
                # Find the first unused color.
                found_valid_color = False
                for color in range(limit-1):
                    if color not in nbr_colors:
                        coloring[u] = color
                        found_valid_color = True
                        break
                if (not found_valid_color):
                    coloring[u] = limit - 1

        for u in G.nodes():
            vertex_multi_colors[u].append(coloring[u]) 

    return vertex_multi_colors


def valid_limited_colorings(G, colorings, limit): 
    for u in G.nodes():
        for v in G[u]:
            if u != v:
                for c1, c2 in zip(colorings[u], colorings[v]):
                    if c1 == c2:
                        if c1 != limit-1:
                            print(u, v, c1, c2)
                            return False
    return True                


def limited_coloring_pruning_test(G, DODGr, k, colorings, num_of_colorings, limit):
    '''
        k - size of cliques being evaluated for pruning savings.
    '''
    total_open_wedges = 0
    combos_pruned_by_number_of_colors = [0] * (num_of_colorings + 1)
    for u in DODGr.nodes():
        # neighbors = [v for v in DODGr.neighbors(u)]
        sorted_neighbors = [n[0] for n in sorted(G.degree(DODGr.neighbors(u)), key = lambda x: x[1])]
        for combo in combinations(sorted_neighbors, 2):
            if combo[1] not in DODGr.neighbors(combo[0]): # Only works for triangle counting now
                total_open_wedges += 1
                for i, (c1, c2) in enumerate(zip(colorings[combo[0]], colorings[combo[1]])):
                    if c1 == c2:
                        if c1 != limit-1: # Can prune because color isn't grey
                            combos_pruned_by_number_of_colors[i+1] += 1
                            break
                # for i in range(num_of_colorings):

                #     colors_of_combo = [colorings[v][i] for v in combo]
                #     if len(colors_of_combo) != len(set(colors_of_combo)):
                #         combos_pruned_by_number_of_colors[i+1] += 1
                #         break
    return combos_pruned_by_number_of_colors, total_open_wedges


def main():

    filenames = [("musae_RU_edges.csv", ","),
                 ("musae_ENGB_edges.csv", ","),
                 ("musae_ES_edges.csv", ","),
                 ("musae_FR_edges.csv", ","),
                 ("Email-Enron.txt", "\t"),
                 ("musae_DE_edges.csv", ","),
                 ("musae_facebook.csv", ","),
                 ("facebook_combined.txt", " ")]

    # filenames = [("musae_facebook.csv", ","),
    #              ("facebook_combined.txt", " ")]

    # filenames = [("musae_facebook.csv", ",")]

    clique_size = 3
    num_of_colorings = 100
    dir_name = "../graphs/"
    graph_pruning_stats = []
    for filename in filenames:
        graph_name = filename[0].split(".")[0]
        print("-" * 80)
        G = nx.read_edgelist(dir_name + filename[0], delimiter=filename[1], nodetype=int)
        print(f"Pruning test for {graph_name} graph") 
        print(f"Nodes: {G.number_of_nodes()}")
        print(f"Edges: {G.number_of_edges()}")
        DODGr = get_DODGr(G)
        max_degree_G = max([v[1] for v in G.degree()])
        max_degree_DODGr = max([v[1] for v in DODGr.out_degree()])
        print(f"Largest degree in original graph: {max_degree_G}")
        print(f"Largest degree in DODGr: {max_degree_DODGr}")
        print(f"Clique size: {clique_size}") 

        # limit = 256
        prob = 0.2
        limit_range = [16, 256, 65536]

        # grey_probabililties = [0.01, 0.05, 0.1, 0.15, 0.2 , 0.25]
        
        val_results = []
        vertex_order = get_DODGr_order(DODGr)
        print("Done getting ordering")
        for l in limit_range:
        # for p in grey_probabililties:
            colorings = get_limited_colorings(G, num_of_colorings, vertex_order, l, prob)
            assert valid_limited_colorings(G, colorings, l), "INVALID COLORING"
            prune_by_color, total_combos = limited_coloring_pruning_test(G, DODGr, clique_size, colorings, num_of_colorings, l)
            percentage_prune = [x/total_combos for x in prune_by_color]
            percent_pruned = prefix_sum(percentage_prune)
            val_results.append(percent_pruned)
        graph_pruning_stats.append(val_results)
    
    print(graph_pruning_stats)

    # Number of sets and subsets
    num_graphs = len(graph_pruning_stats)
    num_r_values = len(graph_pruning_stats[0])
    num_coloring = len(graph_pruning_stats[0][0])

    # Create the plots
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))  # 2 rows, 4 columns for 8 plots
    axes = axes.flatten()  # Flatten for easier indexing

    # Line styles for distinction
    markers = ['o', 's', '^', 'D', 'x']  # Circle, square, triangle, diamond, cross

    limit_range = [16, 256, 65536]
    # probs = [0.01, 0.05, 0.1, 0.15, 0.2 , 0.25]
    for i in range(num_graphs):
        ax = axes[i]  # Select the subplot
        for j in range(num_r_values):
            ax.plot(range(num_coloring), 
                    graph_pruning_stats[i][j], 
                    # label=f'p = {probs[j]}', 
                    label=f'L = {limit_range[j]} ({math.log2(limit_range[j])} bits)', 
                    marker=markers[j % len(markers)],
                    markevery=10)
            # markevery=10  # Show marker every 10 points for clarity
        
        # Add title, legend, and labels
        ax.set_title(filenames[i][0].split('.')[0])
        ax.set_xlabel('Number of Colorings')
        ax.set_ylabel('Percentage of Pruned Open Wedge Checks')
        ax.legend()

        # Adjust layout
        plt.tight_layout()
        plt.savefig('limited_coloring_varying_L_test.png')


if __name__ == "__main__":
    main()