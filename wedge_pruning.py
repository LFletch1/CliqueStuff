import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt
import random

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

# Goal is to produce a diverse set of colorings without altering the vertex ordering
# for which the coloring is based on
    
def get_random_init_coloring(G, vertex_order, init_range):
    '''If a vertex does not have any neighbors that have been colored yet
      initialize it as a random in a select range (colors 1 - 5), color the other
      vertices greedily'''
    colors = {}
    max_degree = max(dict(G.degree()).values())
    for u in vertex_order:
        # Set to keep track of colors of neighbors
        nbr_colors = {colors[v] for v in G[u] if v in colors}
        if len(nbr_colors) == 0:
            colors[u] = random.randint(0, init_range)
        else:
          # Find the first unused color.
          for color in range(max_degree):
              if color not in nbr_colors:
                  break
          colors[u] = color
          if color > max_degree-1:
              print("Color shouldn't be greater than max degree")
              exit()
    return colors

def get_random_relaxed_coloring(G, vertex_order):
    '''Still color vertices based on a vertex ordering
      but allow vertices to not always act the greediest.
      For example say none of vertex u's neighbors are colored 
      1, 3, and 6, then we could allow u to randomly pick 1 and 3,
      maybe flip a coin on being greedy?'''

def propogate_highest_coloring(G, vertex_order): # If ordering is the same, should provide same coloring
    '''Amongst my colored neighbors, find the heighest color k then color
      yourself k + 1'''
    colors = {}
    max_degree = max(dict(G.degree()).values())
    for u in vertex_order:
        # Set to keep track of colors of neighbors
        nbr_colors = {colors[v] for v in G[u] if v in colors}
        if len(nbr_colors) == 0:
            colors[u] = 0
        else:
          # Find the first unused color.
          color = max(nbr_colors) + 1
          colors[u] = color
    

def color_DODGr(G, DODGr, c, strategy=1):
    '''
        Color DODGr with smallest first strategy and for each coloring after that use a random coloring.
        strategy 1 = get_random_init_coloring
    ''' 
    coloring = {}
    DODGr_ordering = get_DODGr_out_degree_order(DODGr)
    for i in range(c): # number of random colorings
        if strategy == 0:
          coloring = nx.greedy_color(G, strategy='random_sequential')
        elif strategy == 1:
          coloring = get_random_init_coloring(G, DODGr_ordering, 10)
        for u in DODGr.nodes():
            for v in DODGr.neighbors(u):
                colorings = DODGr[u][v]["colorings"]
                colorings.append(coloring[v])
                DODGr[u][v]["colorings"] = colorings
                if coloring[u] == coloring[v]:
                    raise Exception("Coloring is improper")           
                

def colors_heuristic_test(DODGr, G, k, c):
    '''
        k - size of cliques being listed.
    '''
    total_combos = 0
    num_of_colorings = c
    combos_pruned_by_number_of_colors = [0] * (num_of_colorings + 1)
    for u in DODGr.nodes():
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


# def strategy_smallest_first(G, colors):
#     return sorted(G, key=G.degree) # sorts least to greatest

def get_DODGr_out_degree_order(DODGr):
    return sorted(DODGr, key=DODGr.out_degree, reverse=True) # Greatest to least
    

# def strategy_largest_DODGr_degree_first():
#     return sorted()

def prefix_sum(nums_list):
    new_list = [0] * len(nums_list)
    new_list[0] = nums_list[0]
    nums_list
    for i in range(1,len(nums_list)):
        new_list[i] = new_list[i-1] + nums_list[i]
    return new_list


def main():
                # ("musae_facebook_edges.csv", ","))
    # filenames = [("musae_PTBR_edges.csv", ","),
    #              ("musae_RU_edges.csv", ","),
    #              ("musae_ENGB_edges.csv", ","),
    #              ("musae_ES_edges.csv", ","),
    #              ("musae_FR_edges.csv", ","),
    #              ("musae_FR_edges.csv", ","),
    #              ("Email-Enron.txt", "\t"),
    #              ("musae_DE_edges.csv", ","),
    #              ("facebook_combined.txt", " ")]
    filenames = [("Email-Enron.txt", "\t")]
    clique_size = 3
    colorings_to_test = 100
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
        for k in range(3,clique_size+1):
            DODGr = get_DODGr(G) # Have to recreate DODGr each time so that colors don't build
            print(f"Clique size k = {k}") 
            color_DODGr(G, DODGr, colorings_to_test, 1)
            prune_by_color, total_combos = colors_heuristic_test(DODGr, G, k, colorings_to_test)
            percentage_prune = [x/total_combos for x in prune_by_color]
            percent_pruned = prefix_sum(percentage_prune)
            plt.plot([x for x in range(colorings_to_test+1)], percent_pruned, label=k)
        print("-" * 80)
        plt.legend()
        plt.title(f"Color pruning of cliques on {graph_name} graph")
        plt.xlabel("Number of colorings")
        plt.ylabel("Percentage of k-1 combos pruned")
        plt.savefig(f"charts/{graph_name}_wedge_pruning.png")
        plt.clf()
            

if __name__ == "__main__":
    main()