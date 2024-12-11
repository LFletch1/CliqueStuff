import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt
import random


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


def get_random_relaxed_coloring(G, vertex_order, n):
    '''Still color vertices based on a vertex ordering
      but allow vertices to not always act the greediest.
      For example say none of vertex u's neighbors are colored 
      1, 3, and 6, then we could allow u to randomly pick 1 and 3,
      maybe flip a coin on being greedy?'''
    colors = {}
    max_degree = max(dict(G.degree()).values())
    for u in vertex_order:
        # Set to keep track of colors of neighbors
        nbr_colors = [colors[v] for v in G[u] if v in colors]
        if len(nbr_colors) == 0:
            colors[u] = 0
        else:
            sorted_nbr_colors = sorted(nbr_colors)
            greedy_options = [0] * n
            i = 0
            for color in range(max_degree): 
                if color not in nbr_colors:
                    greedy_options[i] = color
                    i += 1
                    if i == n:
                        break
            colors[u] = random.choice(greedy_options[:i])
            if color > max_degree-1:
                print("Color shouldn't be greater than max degree")
                exit()
    return colors
     

def get_propogate_highest_coloring(G, vertex_order): # If ordering is the same, should provide same coloring
    '''Amongst my colored neighbors, find the heighest color k then color
      yourself k + 1'''
    colors = {}
    for u in vertex_order:
        # Set to keep track of colors of neighbors
        nbr_colors = {colors[v] for v in G[u] if v in colors}
        if len(nbr_colors) == 0:
            colors[u] = 0
        else:
          # Select color one larger than the largest neighbor color
          color = max(nbr_colors) + 1
          colors[u] = color
    return colors

# def color_DODGr(G, DODGr, c, strategy, vertex_order, arg):
def get_multiple_colorings(G, c, strategy, vertex_order, arg):
    '''
        Color DODGr with smallest first strategy and for each coloring after that use a random coloring.
        strategy 1 = get_random_init_coloring
    ''' 
    vertex_multi_colors = {u : [] for u in G.nodes()}
    # DODGr_ordering = get_DODGr_out_degree_order(DODGr)
    for i in range(c): # number of random colorings
        if strategy == 0:
            coloring = nx.greedy_color(G, strategy='random_sequential')
        elif strategy == 1:
            coloring = get_random_init_coloring(G, vertex_order, arg)
        elif strategy == 2:
            coloring = get_random_relaxed_coloring(G, vertex_order, arg)
        elif strategy == 3:
            coloring = get_propogate_highest_coloring(G, vertex_order) # If ordering is the same, should provide same coloring
        elif strategy == 4:
            coloring = nx.greedy_color(G, strategy='largest_first')     
        for u in G.nodes():
            vertex_multi_colors[u].append(coloring[u]) 

    return vertex_multi_colors

def colors_pruning_test(DODGr, k, colorings, num_of_colorings):
    '''
        k - size of cliques being evaluated for pruning savings.
    '''
    total_combos = 0
    combos_pruned_by_number_of_colors = [0] * (num_of_colorings + 1)
    for u in DODGr.nodes():
        neighbors = [v for v in DODGr.neighbors(u)]
        for combo in combinations(neighbors, k-1):
            total_combos += 1
            for i in range(num_of_colorings):
                # colorings[combo[0]][i] == combo
                # for v in combo:
                #     print(colorings[v])
                colors_of_combo = [colorings[v][i] for v in combo]
                if len(colors_of_combo) != len(set(colors_of_combo)):
                    combos_pruned_by_number_of_colors[i+1] += 1
                    break
    return combos_pruned_by_number_of_colors, total_combos
