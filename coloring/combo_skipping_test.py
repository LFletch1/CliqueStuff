import networkx as nx
from DODGr import *
from graph_coloring import *
from helper import prefix_sum
import matplotlib.pyplot as plt
from combo_generator import combo_generator
import math

# def combo_pruning_check():
def combo_skipping_test(G, DODGr, k, colorings, num_of_colorings):
    '''
        k - size of cliques being evaluated for pruning savings.
    '''
    total_possible_combos = 0
    total_combos_generated = 0
    for u in DODGr.nodes():
        # neighbors = [v for v in DODGr.neighbors(u)]
        sorted_neighbors = [n[0] for n in sorted(G.degree(DODGr.neighbors(u)), key = lambda x: x[1])]
        if len(sorted_neighbors) < k-1:
            continue
        total_possible_combos += math.comb(len(sorted_neighbors), k-1)
        cg = combo_generator(k-1,sorted_neighbors)
        combo = cg.get_next_combo(True, 0, 0)
        # combos_pruned_by_coloring = []

        while combo:
            # print(combo)
            # print(cg.indices)
            combo_valid = True
            idx1 = 0
            idx2 = 0
            for i in range(len(combo)):
                for j in range(i+1, len(combo)): 
                    # print(colorings[i])
                    # print(colorings[j])
                    # input()
                    for c1, c2 in zip(colorings[combo[i]], colorings[combo[j]]):
                        if c1 == c2:
                            idx1 = i
                            idx2 = j
                            combo_valid = False
                            break 
                    if not combo_valid:
                        break
                if not combo_valid:
                    break
            combo = cg.get_next_combo(combo_valid, idx1, idx2)
        total_combos_generated += cg.combos_generated

    total_combos_skipped = total_possible_combos - total_combos_generated

    return total_combos_skipped, total_possible_combos


def main():

    filenames = [("musae_RU_edges.csv", ","),
                 ("musae_ENGB_edges.csv", ","),
                 ("musae_ES_edges.csv", ","),
                 ("musae_FR_edges.csv", ",")]
                #  ("Email-Enron.txt", "\t"),
                #  ("musae_DE_edges.csv", ","),
                #  ("musae_facebook.csv", ","),
                #  ("facebook_combined.txt", " ")]

    # filenames = [("musae_facebook.csv", ",")]

    l_param = 5
    clique_sizes = range(3, 6)
    num_of_colorings = 25
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
        vertex_order = get_DODGr_order(DODGr)
        colorings = get_multiple_colorings(G, num_of_colorings, 2, vertex_order, l_param)

        k_val_results = []
        for k in clique_sizes:
            print(f"Clique size: {k}") 
            total_combos_skipped, total_possible_combos = combo_skipping_test(G, DODGr, k, colorings, num_of_colorings)
            print(f"Total Possible Combos: {total_possible_combos}, Total Combos Skipped: {total_combos_skipped}, {100*(total_combos_skipped/total_possible_combos)}%")
            # percentage_prune = [x/total_combos for x in prune_by_color]
            # percent_pruned = prefix_sum(percentage_prune)
            # k_val_results.append(percent_pruned)
        # graph_pruning_stats.append(k_val_results)
    
    # print(graph_pruning_stats)

    # # Number of sets and subsets
    # num_graphs = len(graph_pruning_stats)
    # num_clique_values = len(graph_pruning_stats[0])
    # num_coloring = len(graph_pruning_stats[0][0])

    # # Create the plots
    # fig, axes = plt.subplots(2, 4, figsize=(16, 8))  # 2 rows, 4 columns for 8 plots
    # axes = axes.flatten()  # Flatten for easier indexing

    # # Line styles for distinction
    # markers = ['o', 's', '^', 'D', 'x']  # Circle, square, triangle, diamond, cross

    # relaxed_range = [1, 3, 5, 10, 20]
    # for i in range(num_graphs):
    #     ax = axes[i]  # Select the subplot
    #     for j in range(num_r_values):
    #         ax.plot(range(num_coloring), 
    #                 graph_pruning_stats[i][j], 
    #                 label=f'L = {relaxed_range[j]}', 
    #                 marker=markers[j % len(markers)],
    #                 markevery=10)
    #         # markevery=10  # Show marker every 10 points for clarity
        
    #     # Add title, legend, and labels
    #     ax.set_title(filenames[i][0].split('.')[0])
    #     ax.set_xlabel('Number of Colorings')
    #     ax.set_ylabel('Percentage of Pruned Open Wedge Checks')
    #     ax.legend()

    #     # Adjust layout
    #     plt.tight_layout()
    #     plt.savefig('new_relaxed_greedy_coloring_test3.png')


if __name__ == "__main__":
    main()