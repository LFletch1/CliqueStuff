import networkx as nx
import statistics
import matplotlib.pyplot as plt

def strategy_smallest_first(G, colors):
    """Returns a list of the nodes of ``G`` in decreasing order by
    degree.
    ``G`` is a NetworkX graph. ``colors`` is ignored.

    """
    return sorted(G, key=G.degree) # sorts least to greatest

def compare_colorings(f, delim=" "):
    G = nx.read_edgelist(f, delimiter=delim, nodetype=int)
    print(G.number_of_nodes()) 
    print(G.number_of_edges())
    coloring_strategies = ('largest_first',
                            'random_sequential',
                            strategy_smallest_first,
                            )
    # 'smallest_last'
    # 'connected_sequential_bfs',
    # 'connected_sequential'
    # 'independent_set',
    # 'DSATUR'
    for strat in coloring_strategies:
        coloring = nx.greedy_color(G, strategy=strat)
        highest_color = 0
        for value in coloring.values():
            if value > highest_color:
                highest_color = value
        print(f"Graph {f} using {strat} strategy colored using {highest_color + 1} colors") # highest color + 1 will equate to total colors used

def minimize_chromatic_degree(filename, delim=" ", random_colorings=100, low_deg_first_coloring = True, high_deg_first_coloring = True):
    '''Using a random ordering for a coloring, continuously find lower chromatic_degree of each node'''
    G = nx.read_edgelist(filename, delimiter=delim, nodetype=int)
    node_chromatic_degree = {n : float('inf') for n in G.nodes()}

    if low_deg_first_coloring:
        coloring = nx.greedy_color(G, strategy=strategy_smallest_first) # Equivalent to DAG Coloring
        for v in G.nodes():
            neighbor_colors = []
            for n in G.neighbors(v):
                neighbor_colors.append(coloring[n])
            chromatic_deg = len(list(dict.fromkeys(neighbor_colors)))
            if chromatic_deg < node_chromatic_degree[v]:
                node_chromatic_degree[v] = chromatic_deg
    
    if high_deg_first_coloring:
        coloring = nx.greedy_color(G, strategy='largest_first')
        for v in G.nodes():
            neighbor_colors = []
            for n in G.neighbors(v):
                neighbor_colors.append(coloring[n])
            chromatic_deg = len(list(dict.fromkeys(neighbor_colors)))
            if chromatic_deg < node_chromatic_degree[v]:
                node_chromatic_degree[v] = chromatic_deg


    for _ in range(random_colorings):
        coloring = nx.greedy_color(G, strategy='random_sequential')
        for v in G.nodes():
            neighbor_colors = []
            for n in G.neighbors(v):
                neighbor_colors.append(coloring[n])
            chromatic_deg = len(list(dict.fromkeys(neighbor_colors)))
            if chromatic_deg < node_chromatic_degree[v]:
                node_chromatic_degree[v] = chromatic_deg
    
    avg_chromatic_deg = sum(node_chromatic_degree.values()) / len(node_chromatic_degree.values())
    max_chromatic_deg = max(node_chromatic_degree.values())
    median_chromatic_deg = statistics.median_high(node_chromatic_degree.values())

    print("-"*10, filename, "-"*10)
    print("Avg Chromatic Degree:", avg_chromatic_deg)
    print("Max Chromatic Degree:", max_chromatic_deg)
    print("Median Chromatic Degree:", median_chromatic_deg)
    print("-"*50)

    return avg_chromatic_deg, max_chromatic_deg, median_chromatic_deg


def main():
    filenames = (("facebook_combined.txt", " "),
                ("Email-Enron.txt", "\t"),
                ("musae_facebook_edges.csv", ","))
                # ("musae_DE_edges.csv", ","),
                # ("musae_PTBR_edges.csv", ","),
                # ("musae_ENGB_edges.csv", ","),
                # ("musae_ES_edges.csv", ","),
                # ("musae_FR_edges.csv", ","),
                # ("musae_RU_edges.csv", ","),
    # for filename_delim in filenames:
    #     compare_colorings(filename_delim[0], filename_delim[1])

    combos = [(i, False, False) for i in range(10,51,10)] + [(i, True, True) for i in range(0,51,10)]
    print(len(combos))
    labels = []
    for combo in combos:
        s = str(combo[0])
        if combo[1]:
            s += "T"
        else:
            s += "F"
        if combo[2]:
            s += "T"
        else:
            s += "F"
        labels.append(s)
    print(len(labels))
    ax = plt.axes()
    ax.set_xticklabels(labels)
    for filename_delim in filenames:
        avg = []
        for combo in combos:
            avg_c_deg, max_c_deg, median_c_deg =minimize_chromatic_degree(filename_delim[0], filename_delim[1], combo[0], combo[1], combo[2])
            avg.append(avg_c_deg)
        plt.plot(avg, label = filename_delim[0])

    plt.xticks([x for x in range(len(combos))])
    plt.xlabel("Coloring Combination")
    plt.legend()
    plt.title("Avg. Chromatic Degree with Different Coloring Method Combinations")
    plt.show()

    ax = plt.axes()
    ax.set_xticklabels(labels)
    for filename_delim in filenames:
        max = []
        for combo in combos:
            avg_c_deg, max_c_deg, median_c_deg =minimize_chromatic_degree(filename_delim[0], filename_delim[1], combo[0], combo[1], combo[2])
            max.append(max_c_deg)
        plt.plot([x for x in range(len(combos))], max, label = filename_delim[0])
    plt.xticks([x for x in range(len(combos))])
    plt.xlabel("Coloring Combination")
    plt.ylabel("Max. Chromatic Degree")
    plt.legend()
    plt.title("Max. Chromatic Degree with Different Coloring Method Combinations")
    plt.show()

if __name__ == "__main__":
    main()