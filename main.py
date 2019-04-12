import pandas as pd
import numpy as np

from lib.Node import Node
from lib.Link import Link
from lib.Flow import TraceFlow
from lib.Network import Network
from lib.utils import *

"""
Topology: 7x7 evenly spaced grid
Why? 7+7+5+5 = 24 edge nodes (x); 5x5=25 inner nodes (o)

z = 0 for all

(x,y)
(0,600) ------> (600,600)
x---x---x---x---x---x---x
|   |   |   |   |   |   |
x---o---o---o---o---o---x
|   |   |   |   |   |   |
x---o---o---o---o---o---x
|   |   |   |   |   |   |
x---o---o---o---o---o---x
|   |   |   |   |   |   |
x---o---o---o---o---o---x
|   |   |   |   |   |   |
x---o---o---o---o---o---x
|   |   |   |   |   |   |
x---x---x---x---x---x---x
(0,0)   ------>   (600,0)

84x2=168 links
"""
#
# Params
#

# node id = ij (like in a matrix, ex 3x3= 0,1,2,10,11,12,20,21,22)
SOURCE=0
DESTINATION=66



trace_file='trace.dat'
mtu=1500
z = 0.0
n = Network()
square_size = 7

# function that checks if node is dead
THRESHOLD=0.05
DEAD_NODE_FLAG=False
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
    return (re ** -1.0) # less energy => large cost

metric = metric_destination_energy

#
# Create network/graph
#
for i in range(square_size):
    for j in range(square_size):
        n.add_node(Node(node_id=int(str(i) + str(j)), position=(i*100.0, j*100.0, 0.0), initial_charge=100.0, up=1.5, down=0.5, update_callback=is_node_dead))
for i in range(square_size):
    for j in range(square_size):
        node = n.get_node(int(str(i) + str(j)))
        if i-1 >= 0:
            n.add_link(Link(metric, from_node=node, to_node=n.get_node(int(str(i-1) + str(j)))))
        if j-1 >= 0:
            n.add_link(Link(metric, from_node=node, to_node=n.get_node(int(str(i) + str(j-1)))))
        if i+1 < square_size:
            n.add_link(Link(metric, from_node=node, to_node=n.get_node(int(str(i+1) + str(j)))))
        if j+1 < square_size:
            n.add_link(Link(metric, from_node=node, to_node=n.get_node(int(str(i) + str(j+1)))))

def generate_sample(network, frame, node_id, next_hop_node_id):
    node = network.get_node(node_id)
    ####### need to add to sample
    local_initial_charge = node.initial_charge
    local_energy_fraction = node.energy_fraction
    #######
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

# TO-DO
# Add flow counter info for nbh and next hop node.
#

    return {
        'frame_type':frame['type'],
        'frame_size':frame['size'],
        'sum_1hop_energy_fraction':agg_1_re_out,
        'sum_1hop_initial_charge':agg_1_ic_out,
        'sum_1hop_current_charge':agg_1_cc_out,
        'sum_1hop_flow_counter':agg_1_fc_out,
        'size_1hop':num_1,
        'sum_2hop_energy_fraction':agg_2_re_out,
        'sum_2hop_initial_charge':agg_2_ic_out,
        'sum_2hop_current_charge':agg_2_cc_out,
        'sum_1hop_flow_counter':agg_2_fc_out,
        'size_2hop':num_2,
        'sum_3hop_energy_fraction':agg_3_re_out,
        'sum_3hop_initial_charge':agg_3_ic_out,
        'sum_3hop_current_charge':agg_3_cc_out,
        'sum_1hop_flow_counter':agg_3_fc_out,
        'size_3hop':num_3,
        'label_energy_fraction':label_re,
        'label_initial_charge':label_ic,
        'label_current_charge':label_cc,
        'label_flow_count':label_fc,
    }

def any_packet_left_in_any_flow(flows):
    for flow in flows:
        if flow.has_packets_left: return True
    return False

# Create flows
flows = []
flows.append(TraceFlow(n.get_node(0), n.get_node(66), trace_file))
flows.append(TraceFlow(n.get_node(6), n.get_node(60), trace_file))

# Consume flows
samples = pd.DataFrame()
while any_packet_left_in_any_flow(flows):
    packets = []
    for flow in flows:

        if flow.has_packets_left == None: continue
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
    for f in flows: f.next()

    # stop simulation if a node dies: time of first death
    if DEAD_NODE_FLAG == True:
        break

samples.to_csv('___.csv', index=False)