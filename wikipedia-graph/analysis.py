import networkx
import matplotlib.pyplot as plt
import dataset

db = dataset.connect('sqlite:///wikipedia.db')

G = networkx.DiGraph()

print('Building graph...')
for page in db['pages'].all():
    G.add_node(page['url'], title=page['title'])

for link in db['links'].all():
    # Only addedge if the endpoints have both been visited
    if G.has_node(link['from_url']) and G.has_node(link['to_url']):
        G.add_edge(link['from_url'], link['to_url'])

# Unclutter by removing unconnected nodes
G.remove_nodes_from(networkx.isolates(G))

# Calculate node betweenness centrality as a measure of importance
print('Calculating betweenness...')
betweenness = networkx.betweenness_centrality(G, endpoints=False)

print('Drawing graph...')

# Sigmoid function to make the colors (a little) more appealing
squish = lambda x : 1 / (1 + 0.5**(20*(x-0.1)))

colors = [(0, 0, squish(betweenness[n])) for n in G.nodes()]
labels = dict((n, d['title']) for n, d in G.nodes(data=True))
positions = networkx.spring_layout(G)

networkx.draw(G, positions, node_color=colors, edge_color='#AEAEAE')

# Draw the labels manually to make them appear above the nodes
for k, v in positions.items():
    plt.text(v[0], v[1]+0.025, s=labels[k], 
             horizontalalignment='center', size=8)

plt.show()