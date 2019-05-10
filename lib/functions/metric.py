def metric_hop(graph, edge):
    return 1.0


def metric_datarate(graph, edge):
    return edge['datarate']


def metric_error(graph, edge):
    return edge['error']


def metric_distance(graph, edge):
    return edge['distance']


def metric_destination_energy(graph, edge):
    to_node = edge
    if graph.nodes[to_node]['energy_fraction'] <= 0.0:
        return float('inf')
    re = graph.nodes[to_node]['energy_fraction']
    return re ** -1.0  # less energy => large cost


def metric_flow_counter(graph, edge):
    to_node = edge['to_node']
    return graph.nodes[to_node]['flow_counter']