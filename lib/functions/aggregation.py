def agg_energy_fraction(graph, nodes):
    """
    Adds the energy_fraction attribute of each node in the set.

    Parameters:
        graph (networkx.DiGraph): The reference graph to perform the operation on.
        nodes (set([int,...])): Set of nodes.
    """
    re = 0
    for node in nodes:
        re += graph.node[node]['energy_fraction']
    return re

def agg_initial_charge(graph, nodes):
    """
    Adds the initial_charge attribute of each node in the set.

    Parameters:
        graph (networkx.DiGraph): The reference graph to perform the operation on.
        nodes (set([int,...])): Set of nodes.
    """
    ic = 0
    for node in nodes:
        ic += graph.node[node]['initial_charge']
    return ic

def agg_current_charge(graph, nodes):
    """
    Adds the remaining_charge attribute of each node in the set.

    Parameters:
        graph (networkx.DiGraph): The reference graph to perform the operation on.
        nodes (set([int,...])): Set of nodes.
    """
    rc = 0
    for node in nodes:
        rc += graph.node[node]['initial_charge'] * graph.node[node]['energy_fraction']
    return rc

def agg_degree(graph, nodes, out=True):
    """
    Adds the out_degree (number of outgoing edges) of each node in the set.

    Parameters:
        graph (networkx.DiGraph): The reference graph to perform the operation on.
        nodes (set([int,...])): Set of nodes.
    """
    d = 0
    for node in nodes:
        if out is True:
            d += graph.out_degree(node)
        else:
            d += graph.in_degree(node)
    return d

def agg_flow_count(graph, nodes, out=True):
    """
    Adds the flow_counter attribute (number of flows going throigh) of each node in the set.

    Parameters:
        graph (networkx.DiGraph): The reference graph to perform the operation on.
        nodes (set([int,...])): Set of nodes.
    """
    fc = 0
    for node in nodes:
        fc += graph.node[node]['flow_counter']
    return fc