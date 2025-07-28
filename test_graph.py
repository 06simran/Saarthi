import matplotlib
matplotlib.use('MacOSX')
  # For macOS/Windows

import matplotlib.pyplot as plt
import networkx as nx

G = nx.DiGraph()
G.add_edge("ISRO", "Chandrayaan-3")
G.add_edge("Chandrayaan-3", "August 2023")

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=12)
plt.title("Test Graph")
plt.show()
