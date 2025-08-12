# import numpy as np
# import matplotlib.pyplot as plt

# # Parameters
# # Shape parameter (exponent - 1)
# a = 3000
# num_samples = 10000000

# # Generate samples
# samples = np.random.power(a, num_samples)
# max_degree = 50000
# min_degree = 2
# new_samples = (max_degree - np.floor(samples * (max_degree - min_degree) + min_degree))

# print(np.average(new_samples))

# c = 25

# only_complement = 0
# only_colors = 0
# hybrid = 0
# total_edges = 0
# for d in new_samples:
#     total_edges += d
#     a = ((d - 1) * d) / 2
#     b = c * d
#     only_complement += a
#     only_colors += b
#     if a < b:
#         hybrid += a
#     else:
#         hybrid += b

# print(f"Storing complement of neighborhoods: {only_complement}")
# print(f"Storing colors of neighborhoods: {only_colors}")
# print(f"Storing colors or complement neighborhoods (hybrid approach): {hybrid}")
# print(f"Hybrid improvement: vs complement = {hybrid / only_complement}, vs color store = {hybrid / only_colors}")
# print(f"Total Edges: {total_edges}, Hybrid / total_edges = {hybrid / total_edges}")


# plt.hist(new_samples, bins=50, density=True, alpha=0.7, color='blue')
# plt.title('Samples from Power Distribution (NumPy)')
# plt.xlabel('Value')
# plt.ylabel('Density')
# plt.savefig("tmp_power_law_distribution")

# import networkx as nx
# from DODGr import *


# def main():

#     filenames = [("musae_RU_edges.csv", ","),
#                  ("musae_ENGB_edges.csv", ","),
#                  ("musae_ES_edges.csv", ","),
#                  ("musae_FR_edges.csv", ","),
#                  ("Email-Enron.txt", "\t"),
#                  ("musae_DE_edges.csv", ","),
#                  ("musae_facebook.csv", ","),
#                  ("facebook_combined.txt", " ")]


#     num_of_colorings = 25
#     dir_name = "./graphs/"
#     for filename in filenames:
        
#         graph_name = filename[0].split(".")[0]
#         print("-" * 80)
#         G = nx.read_edgelist(dir_name + filename[0], delimiter=filename[1], nodetype=int)
#         print(graph_name)
#         print(f"Nodes: {G.number_of_nodes()}")
#         print(f"Edges: {2*G.number_of_edges()}")
#         DODGr = get_DODGr(G)
#         coloring_storage = 0
#         two_hop_storage = 0
#         total_out_edges = 0
#         hybrid_storage = 0
#         for u in DODGr.nodes():
#             i = 0
#             for _,v in DODGr.out_edges(u):
#                 two_hop_storage += DODGr.out_degree(v);   
#                 coloring_storage += num_of_colorings
#                 if DODGr.out_degree(u)  < num_of_colorings:

#                 # if (DODGr.out_degree(u) * (DODGr.out_degree(u) - 1)) / 2  < num_of_colorings:
#                     # hybrid_storage += len(list(set([v2 for v1,v2 in DODGr.out_edges(u)]) & set([v2 for v1,v2 in DODGr.out_edges(v)])))
#                     hybrid_storage += DODGr.out_degree(u) - i
#                 else:
#                     hybrid_storage += num_of_colorings
#                 i = i+1

#             total_out_edges += DODGr.out_degree(u)
            
        
#         print(f"Total Out Edges: {total_out_edges}")       
#         print(f"Total Coloring Storage: {coloring_storage}")       
#         print(f"Total 2-Hop Storage: {two_hop_storage}")       
#         print(f"Hybrid Storage: {hybrid_storage}")       
    
#         # print(f"Largest degree in original graph: {max_degree_G}")
#         # print(f"Largest degree in DODGr: {max_degree_DODGr}")

import networkx as nx
from DODGr import *


def main():

    filenames = [("musae_RU_edges.csv", ","),
                 ("musae_ENGB_edges.csv", ","),
                 ("musae_ES_edges.csv", ","),
                 ("musae_FR_edges.csv", ","),
                 ("Email-Enron.txt", "\t"),
                 ("musae_DE_edges.csv", ","),
                 ("musae_facebook.csv", ","),
                 ("facebook_combined.txt", " ")]


    num_of_colorings = 25
    dir_name = "./graphs/"
    for filename in filenames:
        
        graph_name = filename[0].split(".")[0]
        print("-" * 80)
        G = nx.read_edgelist(dir_name + filename[0], delimiter=filename[1], nodetype=int)
    # Parameters:
    # n = 10000000 # number of nodes
    # m = 8      # number of edges to attach from a new node to existing nodes
    # G = nx.barabasi_albert_graph(n, m)

        print(graph_name)
        print(f"Nodes: {G.number_of_nodes()}")
        print(f"Edges: {2*G.number_of_edges()}")
        print(f"Max Degree: {max([d for _,d in G.degree()])}")
        DODGr = get_DODGr(G)
        print(f"Max Out Degree: {max([d for _,d in DODGr.out_degree()])}")
        coloring_comm = 0
        two_hop_comm = 0
        for u in DODGr.nodes():
            for _,v in DODGr.out_edges(u):
                two_hop_comm += DODGr.out_degree(v);   
                coloring_comm += 2 * num_of_colorings

        print(f"Total Coloring Communication: {coloring_comm}")       
        print(f"Total 2-Hop Out Communication: {two_hop_comm}")       

        largest_color_comm = 0
        largest_two_hop_comm = 0

        largest_out_degree = -1
        largest_out_degree_vertex = -1
        for v,d in DODGr.out_degree():
            if d > largest_out_degree:
                largest_out_degree = d
                largest_out_degree_vertex = v
        
        for _,v in DODGr.out_edges(largest_out_degree_vertex):
            largest_color_comm += num_of_colorings
            largest_two_hop_comm += DODGr.out_degree(v)

        for _,v in DODGr.in_edges(largest_out_degree_vertex):
            largest_color_comm += num_of_colorings
            largest_two_hop_comm += DODGr.out_degree(largest_out_degree_vertex)

        print(f"Communication associated with largest out-degree vertex when Coloring: {largest_color_comm}")       
        print(f"Communication associated with largest out-degree vertex when building 2-hop: {largest_two_hop_comm}")

if __name__ == "__main__":
    main()