import random
from collections import deque

from .sort import *
from .aggregation import *

def parse_trace_line(line):
    """
    Maps a line from a trace file into a dictionary for ease of use.
    
    Parameters:
        line (str): A line from a trace file to be parsed.
    """
    frame_index, frame_type, frame_time, frame_size = [x for x in line.rstrip("\n\r").split('\t') if x]
    return {
        'index': int(frame_index),
        'size': int(frame_size),
        'type': frame_type,
        'time': int(frame_time),
    }


def flow_pair_generator(nodes, number_of_flows):
    """
    Randomly generates non-repeating pairs with no reused item in any pair (i.e. an item only apears once).

    Parameters:
        nodes (list): The list of items (nodes) to select pairs from.
        number_of_flows (int): Number of pairs to generate (must be less than half of len(nodes)).
    """
    if number_of_flows*2 > len(nodes):
        raise ValueError('Infinite loop: (number_of_flows * 2) cannot be larger than len(nodes).')
    # Keep track of already generated pairs
    used_pairs = set()
    used_nodes = set()
    while True:
        pair = random.sample(nodes, 2)
        pair = tuple(sorted(pair))
        if pair[0] not in used_nodes and pair[1] not in used_nodes:
            used_nodes.add(pair[0])
            used_nodes.add(pair[1])
            used_pairs.add(pair)
            if len(used_pairs) == number_of_flows:
                return used_pairs


def distance(a, b):
    """
    Calculates the Euclidean distance between two points 'a' and 'b'.
    
    Parameters:
        a (float, float, float): Cartesian coordinates in the form of (x,y,z).
        b (float, float, float): Cartesian coordinates in the form of (x,y,z).
    """
    return ( (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2 )**0.5



def neighborhood(graph, from_id, hops=1, out=True):
    """
    Retrieves the nth neighborhood set (ids of nodes that are n hops away from from_id).

    Parameters:
        graph (networkx.DiGraph): The reference graph to perform the operation on.
        from_id (int): The unique id of a node in the graph.
        hops (int): The distance from the source in hops.
        out (bool): If False will use incoming links to the source instead of outgoing. Default True.
    """
    visited = set([from_id])
    queue = deque([from_id, None])

    level = 0
    nbh=set([])
    
    while queue:
        vertex = queue.popleft()
        if vertex == None:
            queue.append(None)
            level += 1
            if queue[0] == None:
                return nbh
            else:
                continue
        links = []
        if out is True:
            links = graph.out_edges(vertex)
        else:
            links = graph.in_edges(vertex)
        for link in links:
            nb = link[1]
            if out is False: nb = link[0]
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
                if level+1 == hops: nbh.add(nb)
                elif level+1 > hops: return nbh


def ordinal_label(sorted_list, item):
    """
    Computes the ordinal feature based on sorted list and index.

    Parameters:
        sorted_list (list): Previously sorte list of node ids.
        item (int): An item in the sorted_list (i.e. from which we extract the ordinal feature).
    """
    _sorted_list = [i['id'] for i in sorted_list]
    total = len(sorted_list)
    try:
        index = _sorted_list.index(item)
    except ValueError:
        return -1
    label = float(index) / float(total)
    return label


def any_packet_left_in_any_flow(flows):
    for f in flows:
        if f.has_packets_left:
            return True
    return False


def generate_sample(graph, frame, node_id, next_hop_node_id):
    nbh_1_out = neighborhood(graph, node_id, hops=1)
    nbh_2_out = neighborhood(graph, node_id, hops=2)
    nbh_3_out = neighborhood(graph, node_id, hops=3)

    num_1 = len(nbh_1_out)
    num_2 = len(nbh_2_out)
    num_3 = len(nbh_3_out)

    agg_1_re_out = agg_energy_fraction(graph, nbh_1_out)
    agg_2_re_out = agg_energy_fraction(graph, nbh_2_out)
    agg_3_re_out = agg_energy_fraction(graph, nbh_3_out)

    agg_1_ic_out = agg_initial_charge(graph, nbh_1_out)
    agg_2_ic_out = agg_initial_charge(graph, nbh_2_out)
    agg_3_ic_out = agg_initial_charge(graph, nbh_3_out)

    agg_1_cc_out = agg_current_charge(graph, nbh_1_out)
    agg_2_cc_out = agg_current_charge(graph, nbh_2_out)
    agg_3_cc_out = agg_current_charge(graph, nbh_3_out)

    agg_1_fc_out = agg_flow_count(graph, nbh_1_out)
    agg_2_fc_out = agg_flow_count(graph, nbh_2_out)
    agg_3_fc_out = agg_flow_count(graph, nbh_3_out)

    sorted_re = sort_by_energy_fraction(graph, nbh_1_out)
    sorted_ic = sort_by_initial_charge(graph, nbh_1_out)
    sorted_cc = sort_by_current_charge(graph, nbh_1_out)
    sorted_fc = sort_by_flow_count(graph, nbh_1_out)

    label_re = ordinal_label(sorted_re, next_hop_node_id)
    label_ic = ordinal_label(sorted_ic, next_hop_node_id)
    label_cc = ordinal_label(sorted_cc, next_hop_node_id)
    label_fc = ordinal_label(sorted_fc, next_hop_node_id)

    return {
        'frame_type': frame['type'],
        'frame_size': frame['size'],
        'sum_1hop_energy_fraction': agg_1_re_out,
        'sum_1hop_initial_charge': agg_1_ic_out,
        'sum_1hop_current_charge': agg_1_cc_out,
        'sum_1hop_flow_counter': agg_1_fc_out,
        'size_1hop': num_1,
        'sum_2hop_energy_fraction': agg_2_re_out,
        'sum_2hop_initial_charge': agg_2_ic_out,
        'sum_2hop_current_charge': agg_2_cc_out,
        'sum_2hop_flow_counter': agg_2_fc_out,
        'size_2hop': num_2,
        'sum_3hop_energy_fraction': agg_3_re_out,
        'sum_3hop_initial_charge': agg_3_ic_out,
        'sum_3hop_current_charge': agg_3_cc_out,
        'sum_3hop_flow_counter': agg_3_fc_out,
        'size_3hop': num_3,
        'next_hop_node_id': int(next_hop_node_id),
        'label_energy_fraction': label_re,
        'sorted_energy_fraction': '|'.join(str(i['id']) for i in sorted_re),
        'label_initial_charge': label_ic,
        'sorted_initial_charge': '|'.join(str(i['id']) for i in sorted_ic),
        'label_current_charge': label_cc,
        'sorted_current_charge': '|'.join(str(i['id']) for i in sorted_cc),
        'label_flow_count': label_fc,
        'sorted_flow_count': '|'.join(str(i['id']) for i in sorted_fc),
    }

