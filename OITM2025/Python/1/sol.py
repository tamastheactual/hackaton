def get_addresses(input_path: str) -> tuple[list[str], list[str]]:
    with open(input_path) as file:
        ad = file.readlines()
    ad = [a.strip() for a in ad]
    taxis = ad[:10]
    clients = ad[10:]
    return taxis, clients
...
geolocator = Nominatim(user_agent="Geocoder")
def get_coords(address: str) -> tuple[float, float]:
    co = geolocator.geocode(address)
    return co.latitude, co.longitude
...
def load_map() -> nx.classes.multidigraph.MultiDiGraph:
    G = ox.graph_from_place('Budapest, Hungary', network_type ='drive')
    return G

def shortest_paths(G, taxi_co, client_co) -> np.ndarray:
    distance_matrix = np.zeros((10,10))
    for i, taxi in enumerate(taxi_co):
        orig_node = ox.distance.nearest_nodes(G, taxi[1], taxi[0])
        for j, client in enumerate(client_co):
            dest_node = ox.distance.nearest_nodes(G, client[1], client[0])
            route_length = nx.shortest_path_length(G, orig_node, dest_node, weight='length') / 1000 #km
            distance_matrix[i][j] = route_length
    return distance_matrix
...
def optimal_assignment(distance_matrix, taxi_co, client_co) -> tuple[float, list[tuple]]:
    row_ind, col_ind = linear_sum_assignment(distance_matrix)
    optimal_assignments_co = [(taxi_co[i], client_co[j]) for i, j in zip(row_ind, col_ind)]
    total_distance = distance_matrix[row_ind, col_ind].sum()
    return total_distance, optimal_assignments_co