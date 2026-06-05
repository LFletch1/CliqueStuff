import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt
import random


# Goal is to produce a diverse set of colorings without altering the vertex ordering
# for which the coloring is based on
    
def get_random_init_coloring(G, vertex_order, init_range):
    '''If a vertex does not have any neighbors that have been colored yet
      initialize it as a random color in a select range (colors 1 - 5), color the other
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
      but do no always select the greediest color.
      For example say none of vertex u's neighbors are colored 
      1, 3, and 6, then we could allow u to randomly pick 1 and 3'''
    colors = {}
    max_degree = max(dict(G.degree()).values())
    for u in vertex_order:
        # Set to keep track of colors of neighbors
        nbr_colors = [colors[v] for v in G[u] if v in colors]
        if len(nbr_colors) == 0:
            colors[u] = 0
        else:
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


def get_mis_coloring(G, vertex_order, p):

    colors = {}
    independent_set_size = 0
    GRAY_COLOR = 255
    # nbr_in_mis = {v : False for v in G.nodes()} 
    mis = {v : False for v in G.nodes()} 
    # max_degree = max(dict(G.degree()).values())
    for u in vertex_order:
        # Set to keep track of colors of neighbors
        nbr_colors = [colors[v] for v in G[u] if v in colors]
        nbrs_in_mis = [mis[v] for v in G[u]]

        if True in nbrs_in_mis:
            found_color = False
            for color in range(GRAY_COLOR): 
                if color not in nbr_colors:
                    colors[u] = color
                    found_color = True
                    break   
            if not found_color:
                colors[u] = GRAY_COLOR
            
        elif (random.random() < p):
            # add u to mis and have its neighbors color greedily
            mis[u] = True
            colors[u] = GRAY_COLOR
            independent_set_size += 1
        else:
            colors[u] = GRAY_COLOR
            # found_color = False
            # for color in range(GRAY_COLOR): 
            #     if color not in nbr_colors:
            #         colors[u] = color
            #         found_color = True
            #         break   
            # if not found_color:
            #     colors[u] = GRAY_COLOR
    print(f"Independent Set Size: {independent_set_size}")
    # print(colors)
    # exit()
    return colors



def get_dynamic_relaxed_greedy_colorings(G, c, vertex_order, relax_params):

    vertex_multi_colors = {u : [] for u in G.nodes()}
    coloring = get_random_relaxed_coloring(G, vertex_order, 1)
    for u in G.nodes():
        vertex_multi_colors[u].append(coloring[u]) 

    total_colorings = 1   
    colors_per_param = c-1 // len(relax_params)
    assert colors_per_param > 0, "Must be more colorings that relax parameters!"

    for r in relax_params:  
        if r == relax_params[-1]: # Do last param until required number of colorings met
            while total_colorings < c:
                coloring = get_random_relaxed_coloring(G, vertex_order, r)
                for u in G.nodes():
                    vertex_multi_colors[u].append(coloring[u]) 
                total_colorings += 1
        else:
            for i in range(colors_per_param):
                coloring = get_random_relaxed_coloring(G, vertex_order, r)
                for u in G.nodes():
                    vertex_multi_colors[u].append(coloring[u]) 
                total_colorings += 1

    return vertex_multi_colors


# def color_DODGr(G, DODGr, c, strategy, vertex_order, arg):
def get_multiple_colorings(G, c, strategy, vertex_order, arg):
    '''
        Color DODGr with smallest first strategy and for each coloring after that use a random coloring.
        strategy 1 = get_random_init_coloring
    ''' 
    vertex_multi_colors = {u : [] for u in G.nodes()}
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
        elif strategy == 5:
            coloring = get_mis_coloring(G, vertex_order, arg)
        elif strategy == 6:
            if i == 0:
                coloring = nx.greedy_color(G, strategy='largest_first')     
            if i == 1:
                coloring = get_propogate_highest_coloring(G, vertex_order) # If ordering is the same, should provide same coloring
            elif i in range(2,17):
                coloring = nx.greedy_color(G, strategy='random_sequential')
            elif i in range(17,34):
                coloring = get_random_init_coloring(G, vertex_order, 5)
            elif i in range(34, c):
                coloring = get_random_relaxed_coloring(G, vertex_order, 5)

        for u in G.nodes():
            vertex_multi_colors[u].append(coloring[u]) 

    return vertex_multi_colors


def get_strategy_name(i):
    if i == 0:
        return "random ordering"
    elif i == 1:
        return "random initialization"
    elif i == 2:
        return "relaxed greedy"
    elif i == 3:
        return "propogate hightest"
    elif i == 4:
        return "largest degree first"
    elif i == 5:
        return "ensemble"


def colors_pruning_test(G, DODGr, k, colorings, num_of_colorings):
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
                for i in range(num_of_colorings):
                    colors_of_combo = [colorings[v][i] for v in combo]
                    if len(colors_of_combo) != len(set(colors_of_combo)):
                        combos_pruned_by_number_of_colors[i+1] += 1
                        break
    return combos_pruned_by_number_of_colors, total_open_wedges
