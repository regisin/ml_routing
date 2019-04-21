import pandas as pd
import numpy as np
import networkx as nx

from lib.Node import Node
from lib.Link import Link
from lib.Flow import TraceFlow
from lib.Network import Network
from lib.utils import *

#
# Params
#
trace_file = 'mr_bean.dat'

# function that checks if node is dead
THRESHOLD = 0.05
DEAD_NODE_FLAG = False


def is_node_dead(node):
    if node.energy_fraction <= THRESHOLD:
        print('[INFO] Dead node detected:', node.id)
        global DEAD_NODE_FLAG
        DEAD_NODE_FLAG = True


# function that updates a link cost
def metric_hop(link):
    return 1.0


def metric_datarate(link):
    return link.datarate


def metric_error(link):
    return link.error_probability


def metric_distance(link):
    link.update_distance()
    return link.distance


def metric_destination_energy(link):
    if link.to_node.energy_fraction <= 0.0:
        return float('inf')
    re = link.to_node.energy_fraction
    return re ** -1.0  # less energy => large cost


def metric_flow_counter(link):
    return link.to_node.flow_counter


metric = metric_flow_counter


def generate_sample(network, frame, node_id, next_hop_node_id):
    nbh_1_out = neighborhood(network, node_id, hops=1)
    nbh_2_out = neighborhood(network, node_id, hops=2)
    nbh_3_out = neighborhood(network, node_id, hops=3)

    num_1 = len(nbh_1_out)
    num_2 = len(nbh_2_out)
    num_3 = len(nbh_3_out)

    agg_1_re_out = agg_energy_fraction(network, nbh_1_out)
    agg_2_re_out = agg_energy_fraction(network, nbh_2_out)
    agg_3_re_out = agg_energy_fraction(network, nbh_3_out)

    agg_1_ic_out = agg_initial_charge(network, nbh_1_out)
    agg_2_ic_out = agg_initial_charge(network, nbh_2_out)
    agg_3_ic_out = agg_initial_charge(network, nbh_3_out)

    agg_1_cc_out = agg_current_charge(network, nbh_1_out)
    agg_2_cc_out = agg_current_charge(network, nbh_2_out)
    agg_3_cc_out = agg_current_charge(network, nbh_3_out)

    agg_1_fc_out = agg_flow_count(network, nbh_1_out)
    agg_2_fc_out = agg_flow_count(network, nbh_2_out)
    agg_3_fc_out = agg_flow_count(network, nbh_3_out)

    next_hop_node = n.get_node(next_hop_node_id)

    label_re = ordinal_label(sort_by_energy_fraction(n, nbh_1_out), next_hop_node)
    label_ic = ordinal_label(sort_by_initial_charge(n, nbh_1_out), next_hop_node)
    label_cc = ordinal_label(sort_by_current_charge(n, nbh_1_out), next_hop_node)
    label_fc = ordinal_label(sort_by_flow_count(n, nbh_1_out), next_hop_node)

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
        'label_energy_fraction': label_re,
        'label_initial_charge': label_ic,
        'label_current_charge': label_cc,
        'label_flow_count': label_fc,
    }


def any_packet_left_in_any_flow(flows):
    for f in flows:
        if f.has_packets_left:
            return True
    return False

G = nx.erdos_renyi_graph(64, 0.3)
n = Network()
#
# Create network/graph
#
for v in list(G.nodes):
    n.add_node(Node(node_id=v, initial_charge=150.0, up=1., down=0.7, update_callback=is_node_dead))
for e in list(G.edges):
    f = n.get_node(e[0])
    t = n.get_node(e[1])
    n.add_link(Link(metric, from_node=f, to_node=t))
del G

# Create flows
flows = [
    TraceFlow(n.get_node(1), n.get_node(63), trace_file),
    TraceFlow(n.get_node(5), n.get_node(40), trace_file),
    TraceFlow(n.get_node(25), n.get_node(31), trace_file)
]

samples = pd.DataFrame()
# Consume flows
while any_packet_left_in_any_flow(flows):
    packets = []
    for flow in flows:

        if flow.has_packets_left is None:
            continue
        packets.append(flow.current_packet)

        cost, path = shortest_path(n.graph, flow.from_node.id, flow.to_node.id)

        for node in n.nodes:
            if node.id in path:
                node.is_current_up = True
                node.flow_counter += 1
            else:
                node.is_current_up = False

        next_hop_index = 1
        for node_id in path[0:-1]:
            sample = generate_sample(n, flow.current_packet, node_id, path[next_hop_index])
            next_hop_index += 1
            samples = samples.append(sample, ignore_index=True)

    n.update_with_packets(packets)

    # go to next packet
    for f in flows:
        f.next()

    # stop simulation if a node dies: time of first death
    if DEAD_NODE_FLAG is True:
        break

samples.to_csv('samples.csv', index=False)
