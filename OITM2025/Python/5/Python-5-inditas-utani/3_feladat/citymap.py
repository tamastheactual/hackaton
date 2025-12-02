
import networkx as nx

def load_city_map(file_path):
    '''Load city map from a text file.'''
    edges = []
    with open(file_path, 'r') as f:
        for line in f:
            u, v, w = [int(x) for x in line.strip().split(',')]
            edges.append((u, v, w))
    return edges

def create_graph(edges):
    '''Create a directed graph from edges.'''
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)
    print('Graph created with nodes:', G.nodes())
    return G

def update_graph(G, G0, returned_paths):
    print("Updating graph...")
    #time.sleep(1)
   
    for path in returned_paths:
        path_edges = list(zip(path, path[1:]))
        for u, v in path_edges:
            G[u][v]['weight'] += 1

    for u, v in G.edges:
        lower = G0[u][v]['weight'] - 30
        upper = G0[u][v]['weight'] + 30
        G[u][v]['weight'] = min(upper, max(lower, G[u][v]['weight'] - 10))

    print('Graph updated.')
    print(G.edges(data=True))
    return G

if __name__ == "__main__":
    edges = load_city_map('citymap.txt')
    G = create_graph(edges)
    print("Graph created with nodes:", G.nodes())