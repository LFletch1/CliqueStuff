import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt
import random as rd
from DODGr import *

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
    
def get_random_init_i_set(G, DODGr, vertex_order, p):
    '''
    Use typical greedy MIS algorithm on DAG where a vertex with 0 in-degree is added to the MIS. 
    This addition to the MIS is propogated to its neighbors and they notify their own neighbors that
    they are no longer elgible for being added to the MIS.

    To try to generate random independent sets though, we instead only add those initial vertices with
    a propability of p. Therefore, we are not guarenteed to form an MIS.
    '''
    in_mis = {}

    for v in vertex_order:
        if v not in in_mis:
            if len(list(DODGr.predecessors(v))) == 0:
                if rd.random() <= p:
                    in_mis[v] = True
                    for u in G.neighbors(v):
                        in_mis[u] = False
                else:
                    in_mis[v] = False
            else:
                in_mis[v] = True
                for u in G.neighbors(v):
                    in_mis[u] = False


    total_in_mis = 0
    for v, i in in_mis.items():
        if i == True:
            total_in_mis += 1
    # print(total_in_mis)
    return in_mis

def get_random_i_set(G, DODGr, vertex_order, p):
    '''
    Same as the get_random_init_i_set algorithm but now every time we look to add a vertex to the IS,
    we add it with probability p.
    '''
    in_mis = {}

    for v in vertex_order:
        if v not in in_mis:
            if rd.random() <= p:
                in_mis[v] = True
                for u in G.neighbors(v):
                    in_mis[u] = False
            else:
                in_mis[v] = False

    total_in_mis = 0
    for v, i in in_mis.items():
        if i == True:
            total_in_mis += 1
    # print(total_in_mis)
    return in_mis


def get_random_MIS(G, DODGr, vertex_order, p):
    '''
    Same as the get_random_i_set algorithm, but now once every vertex has had a chance to be added or is 
    eliminated we do a final check to see if a vertex can be added because none of its neighbors are in the 
    set. We will do this in the ordering specified by vertex_order.
    '''
    in_mis = {}

    for v in vertex_order:
        if v not in in_mis:
            if rd.random() <= p:
                in_mis[v] = True
                for u in G.neighbors(v):
                    in_mis[u] = False
            else:
                in_mis[v] = False

    for v in vertex_order:
        found_neighbor_in_mis = False
        for n in G.neighbors(v):
            if in_mis[n] == True:
                found_neighbor_in_mis = True
                break
        if not found_neighbor_in_mis:
            in_mis[v] = True

    return in_mis


def valid_independent_set(G, mis):
    for u in G.nodes():
        for v in G.neighbors(u):
            if mis[u] and mis[v]:
                return False
    return True       


def generate_i_sets_on_DODGr(G, DODGr, strategy, p, s):
    '''
        Generate independent set of vertices (set of vertices where none of the vertices in the set are neighbors)
    ''' 
    i_sets = {n : [] for n in G.nodes()}
    # DODGr_ordering = get_DODGr_out_degree_order(DODGr)
    ordering = get_DODGr_order(DODGr)
    for _ in range(s): # number of random colorings
        if strategy == 0:
            i_set = get_random_init_i_set(G, DODGr, ordering, p)
        elif strategy == 1:
            i_set = get_random_i_set(G, DODGr, ordering, p)
        elif strategy == 2:
            i_set = get_random_MIS(G, DODGr, ordering, p)

        if not valid_independent_set(G, i_set):
            print("Not a valid independent set")       
            exit()

        if len(i_set) != len(ordering):
            print("ERROR: Not every vertex has a status within MIS")       
            exit()

        for u in DODGr.nodes():
            i_sets[u].append(i_set[u])

    return i_sets
                

def indy_set_heuristic_test(DODGr, G, s, i_sets):
    '''
        k - size of cliques being evaluated for pruning savings.
    '''
    total_open_wedges = 0
    combos_pruned_by_number_of_sets = [0] * (s + 1)
    for u in DODGr.nodes():
        # neighbors = [v for v in DODGr.neighbors(u)]
        sorted_neighbors = [n[0] for n in sorted(G.degree(DODGr.neighbors(u)), key = lambda x: x[1])]
        for combo in combinations(sorted_neighbors, 2):
            if combo[1] not in DODGr.neighbors(combo[0]): # Only works for triangle counting now
                total_open_wedges += 1
                for i in range(s):
                    i_s_status_of_combo = [i_sets[v][i] for v in combo]
                    if i_s_status_of_combo[0] == True and i_s_status_of_combo[1] == True:
                        combos_pruned_by_number_of_sets[i+1] += 1
                        break
    return combos_pruned_by_number_of_sets, total_open_wedges


def prefix_sum(nums_list):
    new_list = [0] * len(nums_list)
    new_list[0] = nums_list[0]
    for i in range(1,len(nums_list)):
        new_list[i] = new_list[i-1] + nums_list[i]
    return new_list


def main():
    filenames = [("musae_PTBR_edges.csv", ","),
                 ("musae_RU_edges.csv", ","),
                 ("musae_ENGB_edges.csv", ","),
                 ("musae_ES_edges.csv", ","),
                 ("musae_FR_edges.csv", ","),
                 ("Email-Enron.txt", "\t"),
                 ("musae_DE_edges.csv", ","),
                 ("facebook_combined.txt", " ")]
    # filenames = [("Email-Enron.txt", "\t"),
    #              ("musae_DE_edges.csv", ","),
    #              ("facebook_combined.txt", " ")]
    # filenames = [("musae_PTBR_edges.csv", ",")]
    number_of_mis = 1000
    strategy = 2
    dir_name = "../graphs/"

    fig, axes = plt.subplots(2, 4, figsize=(16, 8))  # 2 rows, 4 columns for 8 plots
    axes = axes.flatten()

    for i, filename in enumerate(filenames):
        graph_name = filename[0].split(".")[0]
        print("-" * 80)
        G = nx.read_edgelist(dir_name + filename[0], delimiter=filename[1], nodetype=int)
        print(f"Pruning test for {graph_name} graph") 
        DODGr = get_DODGr(G)
        max_degree_G = max([v[1] for v in G.degree()])
        max_degree_DODGr = max([v[1] for v in DODGr.out_degree()])
        print(f"Largest degree in original graph: {max_degree_G}")
        print(f"Largest degree in DODGr: {max_degree_DODGr}")
        # for strategy in range(3):
        ax = axes[i]
        for p in [0.05, 0.15, 0.25, 0.5, 0.75]:
            DODGr = get_DODGr(G) # Have to recreate DODGr each time so that MIS reset
            i_sets = generate_i_sets_on_DODGr(G, DODGr, strategy, p, number_of_mis)
            pruned_open_wedges, total_open_wedges = indy_set_heuristic_test(DODGr, G, number_of_mis, i_sets)
            percentage_prune = [x/total_open_wedges for x in pruned_open_wedges]
            percent_pruned = prefix_sum(percentage_prune)
            ax.plot([x for x in range(number_of_mis+1)], percent_pruned, label=p)
        print("-" * 80)
        ax.set_title(graph_name)
        ax.set_xlabel("Number of Independent Sets Generated")
        ax.set_ylabel("Percentage of Open Wedges Pruned")
        ax.legend()
        # plt.title(f"Independent Set Purning on {graph_name} graph")
        # plt.xlabel("Number of Independent Sets Generated")
        # plt.ylabel("Percentage of wedges pruned")
        # plt.savefig(f"../mis_charts/{graph_name}_wedge_pruning_strat2.png")
        # plt.clf()
    plt.tight_layout()
    plt.savefig(f"../mis_charts/mis_wedge_pruning_strat2.png")
            

if __name__ == "__main__":
    main()