import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt

from cleaning_functions import clean_user_names

df = pd.read_csv('data/twitter_retweet_network_data0.csv', sep=';,.', engine='python', names=['tweeter','retweeter'])

df['tweeter'] = df['tweeter'].apply(clean_user_names)
df['retweeter'] = df['retweeter'].apply(clean_user_names)
df2 = df.dropna().sample(1000)

graph = nx.from_pandas_edgelist(df2,'tweeter','retweeter')

positions = nx.spring_layout(graph)
network = nx.draw(graph, pos=positions)
#labels =  nx.draw_networkx_labels(graph, pos=positions)
plt.show()

