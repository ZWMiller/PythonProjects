import graph_builder as gb
import matplotlib.pyplot as plt


def analyze_csv_network_files(n_hubs=20, num_files = None, file_name=None):
    """
    Controller function for the analysis process. User provides a few settings
    and this function will load the graph, setup all edges and nodes, define the
    important hub nodes, and make a plot.

    to be used, not with the parens.
    n_hubs: how many nodes to treat as special "important hubs"
    num_files: how many of the CSV files to read, None defaults to read all
    file_name: string, if provided, saves the network graph to file, otherwise shows the plot

    return: None
    """
    graph = gb.build_graph_from_csvs("data/", num_files=num_files)
    position, network, ax = gb.draw_di_graph(graph)
    hub_nodes = gb.get_hub_nodes(graph, top_n_hubs=n_hubs)

    for user, connections in hub_nodes:
        print("User {} has been retweeted {} times".format(user, connections))

    gb.highlight_important_nodes(graph, position, hub_nodes=hub_nodes, top_n_hubs=n_hubs)

    if type(file_name) == str:
        plt.savefig(file_name, dpi=150)
    else:
        plt.show()

if __name__ == "__main__":
    analyze_csv_network_files(file_name="images/example_network.png", num_files=None)
