import networkx as nx
from DODGr import *
from graph_coloring import *
from helper import *
import numpy as np

def main():
    filenames = [("musae_RU_edges.csv", ","),
                 ("musae_ENGB_edges.csv", ","),
                 ("musae_ES_edges.csv", ","),
                 ("musae_FR_edges.csv", ","),
                 ("Email-Enron.txt", "\t"),
                 ("musae_DE_edges.csv", ","),
                 ("musae_facebook.csv", ","),
                 ("facebook_combined.txt", " ")]
    clique_size = 3
    num_of_colorings = 50
    dir_name = "graphs/"
    pruning_stats = []
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
        k = 3
        print(f"Clique size k = {k}") 
        graph_pruning_stats = []
        strategies = [0,1,2,5]
        for strat in strategies:
            colorings = get_multiple_colorings(G, num_of_colorings, strat, get_DODGr_out_degree_order(DODGr), 5)
            prune_by_color, total_combos = colors_pruning_test(DODGr, k, colorings, num_of_colorings)
            percentage_prune = [x/total_combos for x in prune_by_color]
            percent_pruned = prefix_sum(percentage_prune)
            graph_pruning_stats.append(percent_pruned)
        pruning_stats.append(graph_pruning_stats)


    # Number of sets and subsets
    num_graphs = len(pruning_stats)
    num_strategies = len(pruning_stats[0])
    num_coloring = len(pruning_stats[0][0])

    # Create the plots
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))  # 2 rows, 4 columns for 8 plots
    axes = axes.flatten()  # Flatten for easier indexing

    # Line styles for distinction
    markers = ['o', 's', '^', 'D', 'x']  # Circle, square, triangle, diamond, cross

    strategies = [0, 1, 2, 5]
    for i in range(num_graphs):
        ax = axes[i]  # Select the subplot
        for j in range(num_strategies):
            ax.plot(range(num_coloring), 
                    pruning_stats[i][j], 
                    label=f'{get_strategy_name(strategies[j])}', 
                    marker=markers[j % len(markers)],
                    markevery=5)
        
        # Add title, legend, and labels
        ax.set_title(filenames[i][0].split('.')[0])
        ax.set_xlabel('Number of Colorings')
        ax.set_ylabel('Percentage of Pruned Wedge Checks')
        ax.legend()

        # Adjust layout
        plt.tight_layout()
        plt.savefig('strategy_comparison.png')


if __name__ == "__main__":
    main()