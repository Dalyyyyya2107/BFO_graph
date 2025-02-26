from model import Population
import pickle  # Load the saved road network graph
import networkx as nx
import os
import matplotlib.pyplot as plt  
import matplotlib.animation as animation

# --- LOAD ROAD NETWORK ---
bacteria_traffic_path = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(bacteria_traffic_path, "montreal_road_graph.gpickle")

# Load the saved graph file
with open(file_path, "rb") as f:
    graph = pickle.load(f)

# --- SIMULATION PARAMETERS ---
num_steps = 150  # Total number of time steps
num_agents = 30  # Number of bacteria
seed = 42  # Random seed

# --- INITIALIZE SIMULATION ---
world = Population(num_steps, num_agents, graph, seed=seed)
world.init_agents()  # Place bacteria in random positions

# Get node positions for visualization
pos = {node: (graph.nodes[node]['x'], graph.nodes[node]['y']) for node in graph.nodes}

# for animation
fig, ax = plt.subplots(figsize=(10, 10))
nx.draw(graph, pos, ax=ax, node_size=2, edge_color='gray', alpha=0.3, linewidths=0.3)

# Store agent positions
trajectories = {agent.unique_id: [] for agent in world.schedule.agents}

# scatter plot for bacteria
scat = ax.scatter([], [], c='red', s=8, edgecolors='black', label="Bacteria")

def update(frame):
    """ Updates the positions of bacteria in real-time. """
    world.step()  # Move bacteria

    x_vals, y_vals = [], []
    for agent in world.schedule.agents:
        node = agent.node  # Get current intersection
        if node in pos:
            x_vals.append(pos[node][0])
            y_vals.append(pos[node][1])
            trajectories[agent.unique_id].append(pos[node])  # Store movement history

    # Clear and redraw plot
    ax.clear()
    nx.draw(graph, pos, ax=ax, node_size=2, edge_color='gray', alpha=0.3, linewidths=0.3)
    ax.scatter(x_vals, y_vals, c='red', s=8, edgecolors='black', label="Bacteria")

    return scat,

# --- RUN ANIMATION ---
ani = animation.FuncAnimation(fig, update, frames=num_steps, interval=30, blit=False)

plt.title("Random Bacteria Movement in Montreal Road Network")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend()
plt.show()
