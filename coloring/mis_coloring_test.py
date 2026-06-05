import networkx as nx
from DODGr import *
from graph_coloring import *
from helper import prefix_sum
import matplotlib.pyplot as plt


def limited_coloring_pruning_test(G, DODGr, colorings, num_of_colorings, limit):
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
        # relaxed_range = [1, 3, 5, 10, 20]
        p_range = [0.05, 0.1, 0.2, 0.3, 0.5]
        rx_val_results = []
        vertex_order = get_DODGr_order(DODGr)
        print("Done getting ordering")
        for p in p_range:
            colorings = get_multiple_colorings(G, num_of_colorings, 5, vertex_order, p)
            # prune_by_color, total_combos = colors_pruning_test(G, DODGr, clique_size, colorings, num_of_colorings)
            prune_by_color, total_combos = limited_coloring_pruning_test(G, DODGr, colorings, num_of_colorings, 256)
            percentage_prune = [x/total_combos for x in prune_by_color]
            percent_pruned = prefix_sum(percentage_prune)
            rx_val_results.append(percent_pruned)
        graph_pruning_stats.append(rx_val_results)
    
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

    # relaxed_range = [1, 3, 5, 10, 20]
    p_range = [0.05, 0.1, 0.2, 0.3, 0.5]
    for i in range(num_graphs):
        ax = axes[i]  # Select the subplot
        for j in range(num_r_values):
            ax.plot(range(num_coloring), 
                    graph_pruning_stats[i][j], 
                    label=f'p = {p_range[j]}', 
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
        plt.savefig('mis_coloring_test.png')


if __name__ == "__main__":
    main()