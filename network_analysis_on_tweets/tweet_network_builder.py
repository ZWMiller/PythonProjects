import graph_builder as gb
import matplotlib.pyplot as plt

graph = gb.build_graph_from_csvs("data/", num_files=3)
position, network, ax = gb.draw_di_graph(graph)
for user, connections in gb.get_hub_nodes(graph):
    print("User {} has {} retweets in the dataset".format(user, connections))
gb.highlight_important_nodes(graph, position)
plt.savefig("images/example_network.png")

