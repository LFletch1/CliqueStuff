import networkx as nx
from DODGr import *
from graph_coloring import *
from helper import prefix_sum
import matplotlib.pyplot as plt

def main():

    filenames = [("musae_RU_edges.csv", ","),
                 ("musae_ENGB_edges.csv", ","),
                 ("musae_ES_edges.csv", ","),
                 ("musae_FR_edges.csv", ","),
                 ("Email-Enron.txt", "\t"),
                 ("musae_DE_edges.csv", ","),
                 ("musae_facebook.csv", ","),
                 ("facebook_combined.txt", " ")]

    # filenames = [("musae_RU_edges.csv", ",")]

    clique_size = 3
    num_of_colorings = 100
    dir_name = "../graphs/"

    # graph_pruning_stats = []
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))  # 2 rows, 4 columns for 8 plots
    axes = axes.flatten()  # Flatten for easier indexing

    for i, filename in enumerate(filenames):
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
        # relaxed_range = [2, 3, 4, 5, 8, 10, 16]
        relaxed_range = [i for i in range(2,11)]
        vertex_order = get_DODGr_order(DODGr)
        print("Done getting ordering")
        colorings = get_dynamic_relaxed_greedy_colorings(G, num_of_colorings, vertex_order, relaxed_range)
        prune_by_color, total_combos = colors_pruning_test(G, DODGr, clique_size, colorings, num_of_colorings)
        percentage_prune = [x/total_combos for x in prune_by_color]
        percent_pruned = prefix_sum(percentage_prune)
        # graph_pruning_stats.append(percent_pruned)

        ax = axes[i]  # Select the subplot
        ax.plot(range(num_of_colorings+1), 
                percent_pruned,
                label=f"{relaxed_range}", 
                markevery=10)

        ax.set_title(filenames[i][0].split('.')[0])
        ax.set_xlabel('Number of Colorings')
        ax.set_ylabel('Percentage of Pruned Open Wedge Checks')
        ax.legend()
    
    # Adjust layout
    plt.tight_layout()
    plt.savefig('dynamic_relaxed_greedy_coloring.png')
    
    # print(graph_pruning_stats)

    # Number of sets and subsets
    # num_graphs = len(graph_pruning_stats)
    # num_r_values = len(graph_pruning_stats[0])
    # num_coloring = len(graph_pruning_stats[0][0])

    # Create the plots
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