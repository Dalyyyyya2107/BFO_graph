import osmnx as ox  # Library to fetch OpenStreetMap data
import networkx as nx  # Library to handle graph structures
import pickle  # Library to save/load the graph
import os
import matplotlib.pyplot as plt 

# Define the area of interest (Dtown MTL)
place_name = "Downtown Montreal, Quebec, Canada"

# Extract the road network as a directed graph 
graph = ox.graph_from_place(place_name, network_type='drive')

# Ensure that the graph is connceted 
largest_component = max(nx.connected_components(graph.to_undirected()), key=len)
G = graph.subgraph(largest_component).copy()

# Saving the graph 
save_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "montreal_road_graph.gpickle")
with open(save_path, "wb") as f:
    pickle.dump(G, f)

# Visualization
fig, ax = plt.subplots(figsize=(10, 10))
ox.plot_graph(G, ax=ax, node_size=10, edge_linewidth=1, bgcolor="white")
plt.title("Road Network of Downtown Montreal")
plt.show()
