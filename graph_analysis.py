# handling plots
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# for network creation
import networkx as nx

from network_building import graph
from operator import itemgetter

# Number of nodes and edges
print("There are", graph.number_of_nodes(), " nodes and ", graph.number_of_edges(), "edges present in the Graph")

# Minimum / Maximum / Average / Most frequest degrees
degrees = [val for (node, val) in graph.degree()]
print("The maximum degree of the Graph is ", np.max(degrees))
print("The minimum degree of the Graph is ", np.min(degrees))
print("The average degree of the nodes in the Graph is ", np.mean(degrees))
print("The most frequent degree of the nodes found in the Graph is ", stats.mode(degrees)[0][0])

# Check if the graph is connected
if nx.is_connected(graph):
    print("The graph is connected")
else:
    print("The graph is not connected")

# Number of connected components
print("There are ", nx.number_connected_components(graph), " connected components in the Graph")

# Largest connected component
largest_subgraph = graph.subgraph(max(nx.connected_components(graph), key=len))
print("There are ", largest_subgraph.number_of_nodes(), " nodes and ", largest_subgraph.number_of_edges(), " edges present in the largest component of the Graph")

# Average clustering coefficient & transitivity of the largest connected componet
print("The average clustering coefficient is ", nx.average_clustering(largest_subgraph), " in the largest subgraph")
print("The transitivity of the largest subgraph is ", nx.transitivity(largest_subgraph))

# Diameter of the graph & average distance between any two nodes
print("The diameter of our Graph is ", nx.diameter(largest_subgraph))
print("The average distance between any two nodes is ", nx.average_shortest_path_length(largest_subgraph))

# Degree centrality (no. of ties)
graph_centrality = nx.degree_centrality(largest_subgraph)
max_de = max(graph_centrality.items(), key=itemgetter(1))
print("The node with id ", max_de[0], " has a degree centrality of ", max_de[1], " which is the maximum of the Graph")

# Closeness (average farness [inverse distance] to all other nodes)
graph_closeness = nx.closeness_centrality(largest_subgraph)
max_clo = max(graph_closeness.items(), key=itemgetter(1))
print("The node with id ", max_clo[0], " has a closeness centrality of ", max_clo[1], " which is the maximum of the Graph")

# Betweenness (the influencer of the graph)
graph_betweenness = nx.betweenness_centrality(largest_subgraph, normalized=True, endpoints=False)
max_bet = max(graph_betweenness.items(), key=itemgetter(1))
print("The node with id ", max_bet[0], " has a betweenness centrality of ", max_bet[1], " which is the maximum of the Graph")

# The largest connected component
# fig = plt.figure(figsize=(100, 100))
# nx.draw_spring(largest_subgraph, node_size=10)
# plt.show()

# The entire graph
# fig = plt.figure(figsize=(100, 100))
# nx.draw_spring(graph, node_size=10)
# plt.show()
