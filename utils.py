# from classes import Node, Link, Network

def parse_trace_line(line):
    frame_index, frame_type, frame_time, frame_size = [x for x in line.rstrip("\n\r").split('\t') if x]
    return {
        'frame_index': int(frame_index),
        'frame_size': int(frame_size),
        'frame_type': frame_type,
        'frame_time': int(frame_time),
    }

def distance(a,b):
    return ( (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2 )**0.5





def get_agg_remaining_energy(network, node_id_set):
    re = 0
    for _id in node_id_set:
        node = network.get_node_by_id(_id)
        re += node.remaining_energy
    return re
def get_agg_initial_charge(network, node_id_set):
    ic = 0
    for _id in node_id_set:
        node = network.get_node_by_id(_id)
        ic += node.initial_charge
    return ic
def get_agg_remaining_charge(network, node_id_set):
    rc = 0
    for _id in node_id_set:
        node = network.get_node_by_id(_id)
        rc += node.initial_charge * node.remaining_energy
    return rc
def get_agg_out_degree(network, node_id_set):
    od = 0
    for _id in node_id_set:
        od += network.get_node_out_degree(_id)
    return od
def get_agg_in_degree(network, node_id_set):
    ind = 0
    for _id in node_id_set:
        ind += network.get_node_in_degree(_id)
    return ind

def sort_by_remaining_energy(network, node_id_set):
    nodes = []
    for _id in node_id_set:
        nodes.append(network.get_node_by_id(_id))
    return sorted(nodes, key=lambda x: x.remaining_energy)
def sort_by_initial_charge(network, node_id_set):
    nodes = []
    for _id in node_id_set:
        nodes.append(network.get_node_by_id(_id))
    return sorted(nodes, key=lambda x: x.initial_charge)
def sort_by_remaining_charge(network, node_id_set):
    nodes = []
    for _id in node_id_set:
        nodes.append(network.get_node_by_id(_id))
    return sorted(nodes, key=lambda x: x.remaining_charge)

def pct_label(node_list, next_hop):
    total = len(node_list)
    index = node_list.index(next_hop)
    label = float(index)/float(total)
    return label