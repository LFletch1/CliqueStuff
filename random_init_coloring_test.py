

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