import json
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from nlp_engine import extract_entities

# Load extracted entity data
def load_entities(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Build a clean and focused knowledge graph
def build_knowledge_graph(data):
    G = nx.DiGraph()

    for item in data:
        main_text = item["text"]
        entities = item["entities"]

        product = None
        date = None

        for entity, label in entities:
            if len(entity.strip()) < 4:
                continue  # Skip short/noisy text
            G.add_node(entity, label=label)

            if label == "PRODUCT":
                product = entity
            elif label == "DATE":
                date = entity

        # Connect mission name to its launch date
        if product and date:
            G.add_edge(product, date, relation="launch_date")

    return G

# Display the graph with colors by entity type
def show_graph(G):
    if not G.nodes:
        print("⚠️ Graph is empty")
        return

    pos = nx.spring_layout(G, k=0.7)
    plt.figure(figsize=(12, 8))

    # Assign node colors based on label
    colors = []
    for node in G.nodes(data=True):
        label = node[1].get("label", "")
        if label == "DATE":
            colors.append("orange")
        elif label == "PRODUCT":
            colors.append("lightgreen")
        else:
            colors.append("skyblue")

    nx.draw(G, pos, with_labels=True, node_color=colors, edge_color="gray", node_size=1500, font_size=10)
    edge_labels = nx.get_edge_attributes(G, 'relation')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Saarthi Knowledge Graph: Mission Launches")
    plt.tight_layout()
    plt.savefig("data/saarthi_graph.png", dpi=300)


# Main logic
if __name__ == "__main__":
    data = load_entities("data/isro_updates.json")  # still using raw scraped headlines
    results = extract_entities(data)                # re-extracts entities from text

    # Save structured entities to file (optional)
    with open("data/isro_entities.json", "w") as f:
        json.dump(results, f, indent=2)

    G = build_knowledge_graph(results)
    print(f"✅ Graph has {len(G.nodes())} nodes and {len(G.edges())} edges.")
    show_graph(G)
