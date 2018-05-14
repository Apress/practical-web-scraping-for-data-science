import pandas as pd
import networkx as nx
from networkx.readwrite.gexf import write_gexf

df = pd.read_pickle('sp500.pkl')

G = nx.Graph()

for row in df.itertuples():
    G.add_node(row.symbol, type='company')
    G.add_node(row.Name,type='officer')
    G.add_edge(row.symbol, row.Name)
 
write_gexf(G, 'graph.gexf')