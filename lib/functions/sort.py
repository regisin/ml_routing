def sort_by_energy_fraction(graph, nodes):
    """
    Returns a sorted (ascending) list based on the energy_fraction attribute of each node in the set.

    Parameters:
        graph (networkx.DiGraph): The reference graph to perform the operation on.
        nodes (set([int,...])): Set of nodes.
    """
    sorted_nodes = []
    for node in nodes:
        sorted_nodes.append(graph.node[node])
    return sorted(sorted_nodes, key=lambda x: x['energy_fraction'])

def sort_by_initial_charge(graph, nodes):
    """
    Returns a sorted (ascending) list based on the initial_charge attribute of each node in the set.

    Parameters:
        graph (networkx.DiGraph): The reference graph to perform the operation on.
        nodes (set([int,...])): Set of nodes.
    """
    sorted_nodes = []
    for node in nodes:
        sorted_nodes.append(graph.node[node])
    return sorted(sorted_nodes, key=lambda x: x['initial_charge'])

def sort_by_current_charge(graph, nodes):
    """
    Returns a sorted (descending) list based on the current_charge attribute of each node in the set.

    Parameters:
        graph (networkx.DiGraph): The reference graph to perform the operation on.
        nodes (set([int,...])): Set of nodes.
    """
    sorted_nodes = []
    for node in nodes:
        sorted_nodes.append(graph.node[node])
    return sorted(sorted_nodes, key=lambda x: 1./(1.+x['current_charge']))

def sort_by_flow_count(graph, nodes):
    """
    Returns a sorted (ascending) list based on the flow_counter attribute of each node in the set.

    Parameters:
        graph (networkx.DiGraph): The reference graph to perform the operation on.
        nodes (set([int,...])): Set of nodes.
    """
    sorted_nodes = []
    for node in nodes:
        sorted_nodes.append(graph.node[node])
    return sorted(sorted_nodes, key=lambda x: x['flow_counter'])