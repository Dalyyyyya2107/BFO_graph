#==== This code generates the graphs for the redesigns ====

import networkx as nx
import matplotlib.pyplot as plt
import csv
import os

# === Current Montreal metro ===
def build_metro_graph(csv_path):
    stations_by_line = {}
    station_positions = {}
    G = nx.Graph()

    with open(csv_path, newline='', encoding='ISO-8859-1') as csvfile:
        raw_reader = csv.reader(csvfile, delimiter=';')
        headers = [h.strip() for h in next(raw_reader)]
        csvfile.seek(0)
        reader = csv.DictReader(csvfile, fieldnames=headers, delimiter=';')
        next(reader)

        for row in reader:
            try:
                line = row['line'].strip().title()
                station = row['station'].strip()
                lat = float(row['latitude'].replace(',', '.').strip())
                lon = -abs(float(row['longitude'].replace(',', '.').strip()))
                if not (45 <= lat <= 46 and -74 <= lon <= -73):
                    continue
                station_positions[station] = (lon, lat)
                stations_by_line.setdefault(line, []).append(station)
            except:
                continue

    line_colors = {
        "Green Line": "green", "Orange Line": "orange",
        "Blue Line": "blue", "Yellow Line": "yellow"
    }

    for station, pos in station_positions.items():
        G.add_node(station, pos=pos)

    for line, station_list in stations_by_line.items():
        for i in range(len(station_list) - 1):
            if station_list[i] in G and station_list[i + 1] in G:
                G.add_edge(
                    station_list[i], station_list[i + 1],
                    color=line_colors.get(line, 'gray')
                )
    return G

# Redesigns Metro ===>
def build_redesign_graph(csv_path):
    G = nx.Graph()
    positions_by_line = {}

    with open(csv_path, newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        reader.fieldnames = [h.strip() for h in reader.fieldnames]    # we can later on add station names if desired 
        for row in reader:
            try:
                line = row['line'].strip().title()
                lat = float(row['latitude'].replace(',', '.').strip())
                lon = -abs(float(row['longitude'].replace(',', '.').strip()))
                if not (45 <= lat <= 46 and -74 <= lon <= -73):
                    continue
                positions_by_line.setdefault(line, []).append((lon, lat))
            except:
                continue

    line_colors = {
        "Green Line": "green", "Orange Line": "orange",
        "Blue Line": "blue", "Yellow Line": "yellow"
    }

    for line, coords in positions_by_line.items():
        prev = None
        for i, pos in enumerate(coords):
            node_id = f"{line}_{i}"
            G.add_node(node_id, pos=pos)
            if prev:
                G.add_edge(prev, node_id, color=line_colors.get(line, 'gray'))
            prev = node_id

    return G

# File paths
base_path = os.path.dirname(__file__)
file_configs = {
    "Current Montreal Metro": os.path.join(base_path, "metro_stations.csv"),
    "Redesign #1 of Montreal Metro": os.path.join(base_path, "redesign_1.csv"),
    "Redesign #2 of Montreal Metro": os.path.join(base_path, "redesign_2.csv"),
    "Redesign #3 of Montreal Metro": os.path.join(base_path, "redesign_3.csv"),
    "Redesign #4 of Montreal Metro": os.path.join(base_path, "redesign_4.csv"),
}

# display  
for title, path in file_configs.items():
    graph = build_metro_graph(path) if "Current" in title else build_redesign_graph(path)
    if not graph:
        continue

    pos = nx.get_node_attributes(graph, 'pos')
    fig, ax = plt.subplots(figsize=(12, 10))

    if graph.edges:
        nx.draw_networkx_nodes(graph, pos, node_size=10, node_color='black', alpha=0.8, ax=ax)
        edge_colors = [d['color'] for _, _, d in graph.edges(data=True)]
        nx.draw_networkx_edges(graph, pos, edge_color=edge_colors, width=2, alpha=0.5, ax=ax)
    elif graph.nodes:
        xs, ys = zip(*pos.values())
        ax.scatter(xs, ys, color='black', s=10)
        ax.set_title(f"{title} (points only)", fontsize=14)
    else:
        ax.set_title(f"{title} (no data)", fontsize=14)

    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_aspect('equal')
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()
