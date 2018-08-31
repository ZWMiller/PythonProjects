import graph_builder as gb
import matplotlib.pyplot as plt

n_hubs = 20
graph = gb.build_graph_from_csvs("data/", num_files=None)
position, network, ax = gb.draw_di_graph(graph)

for user, connections in gb.get_hub_nodes(graph, top_n_hubs=n_hubs):
    print("User {} has {} retweets in the dataset".format(user, connections))

gb.highlight_important_nodes(graph, position, top_n_hubs=n_hubs)
plt.savefig("images/example_network.png")

