# create network
# load trace
# compute dijkstra+update network state for each packet
import csv
import json
import pandas as pd
import numpy as np
from classes import Node, Link, Network
from utils import parse_trace_line, get_agg_in_degree, get_agg_out_degree,\
                    get_agg_initial_charge, get_agg_remaining_energy, get_agg_remaining_charge,\
                    sort_by_remaining_energy, sort_by_initial_charge, sort_by_remaining_charge,\
                    pct_label

"""
Topology: 7x7 evenly spaced grid
Why? 7+7+5+5 = 24 edge nodes (x); 5x5=25 inner nodes (o)

z = 0 for all

(x,y)
(0,600) ----> (600,600)
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
(0,0) ----> (600,0)

84x2=168 links
"""
#
# Params
#

# Do this for ALL pairs
# node id = ij (like in a matrix, ex 3x3= 0,1,2,10,11,12,20,21,22)
SOURCE=0
DESTINATION=33



trace_file='trace.dat'
mtu=1500
z = 0.0
n = Network()
square_size = 4

# dead node found
def dead_node_removed():
    pass

# function that updates a link cost
def metric_hop(link):
    return 1
def metric_datarate(link):
    return link.datarate
def metric_error(link):
    return link.error_probability
def metric_distance(link):
    link.update_distance()
    return link.distance
def metric_destination_energy(link):
    if link._to.remaining_energy <= 0.0:
        return float('inf')
    return link._to.remaining_energy ** -1.0 # less energy => large cost

metric = metric_destination_energy


#
# Create network/graph
#
for i in range(square_size):
    for j in range(square_size):
        n.add_node(node=Node(_id=int(str(i) + str(j)), position=(i*100.0, j*100.0, z)))

for i in range(square_size):
    for j in range(square_size):
        node = n.get_node_by_id(int(str(i) + str(j)))
        if i-1 >= 0:
            n.add_link(link=Link(metric, _from=node, _to=n.get_node_by_id(int(str(i-1) + str(j)))))
        if j-1 >= 0:
            n.add_link(link=Link(metric, _from=node, _to=n.get_node_by_id(int(str(i) + str(j-1)))))
        if i+1 < square_size:
            n.add_link(link=Link(metric, _from=node, _to=n.get_node_by_id(int(str(i+1) + str(j)))))
        if j+1 < square_size:
            n.add_link(link=Link(metric, _from=node, _to=n.get_node_by_id(int(str(i) + str(j+1)))))

samples = pd.DataFrame()
with open(trace_file) as f:
    i = 0
    for line in f:
        frame = parse_trace_line(line)
        # "transmit the frame"
        # - calculate shortest path
        cost, path = n.shortest_path(source=n.get_node_by_id(SOURCE), destination=n.get_node_by_id(DESTINATION))
        # - save network state (topology, node state, link state, frame)
        for node in n.nodes:
            node.current_up=True if node.id in path else False
        
        # generate state and/or sample entries
        # n_state, l_state = n.get_state()
        nbh_1_out = n.get_out_nth_neighborhood_set(SOURCE, hops=1)
        nbh_2_out = n.get_out_nth_neighborhood_set(SOURCE, hops=2)
        nbh_3_out = n.get_out_nth_neighborhood_set(SOURCE, hops=3)

        num_1 = len(nbh_1_out)
        num_2 = len(nbh_2_out)
        num_3 = len(nbh_3_out)


        agg_1_re_out = get_agg_remaining_energy(n, nbh_1_out)
        agg_2_re_out = get_agg_remaining_energy(n, nbh_2_out)
        agg_3_re_out = get_agg_remaining_energy(n, nbh_3_out)

        agg_1_ic_out = get_agg_initial_charge(n, nbh_1_out)
        agg_2_ic_out = get_agg_initial_charge(n, nbh_2_out)
        agg_3_ic_out = get_agg_initial_charge(n, nbh_3_out)

        agg_1_rc_out = get_agg_remaining_charge(n, nbh_1_out)
        agg_2_rc_out = get_agg_remaining_charge(n, nbh_2_out)
        agg_3_rc_out = get_agg_remaining_charge(n, nbh_3_out)
        
        next_hop_node = n.get_node_by_id(path[1])

        label_re = pct_label(sort_by_remaining_energy(n, nbh_1_out), next_hop_node)
        label_ic = pct_label(sort_by_initial_charge(n, nbh_1_out), next_hop_node)
        label_rc = pct_label(sort_by_remaining_charge(n, nbh_1_out), next_hop_node)

        sample={
            'frame_type':frame['frame_type'],
            'frame_size':frame['frame_size'],
            # 'local_remaining_energy': n.get_node_by_id(SOURCE).remaining_energy,
            # 'local_remaining_energy': n.get_node_by_id(SOURCE).remaining_energy,
            # 'local_remaining_energy': n.get_node_by_id(SOURCE).remaining_energy,
            'sum_1hop_remaining_energy':agg_1_re_out,
            'sum_1hop_initial_charge':agg_1_ic_out,
            'sum_1hop_remaining_charge':agg_1_rc_out,
            'size_1hop':num_1,
            'sum_2hop_remaining_energy':agg_2_re_out,
            'sum_2hop_initial_charge':agg_2_ic_out,
            'sum_2hop_remaining_charge':agg_2_rc_out,
            'size_2hop':num_2,
            'sum_3hop_remaining_energy':agg_3_re_out,
            'sum_3hop_initial_charge':agg_3_ic_out,
            'sum_3hop_remaining_charge':agg_3_rc_out,
            'size_3hop':num_3,
            'label_remaining_energy':label_re,
            'label_initial_charge':label_ic,
            'label_remaining_charge':label_rc
        }

        samples = samples.append(sample, ignore_index=True)

        # update network state for next round
        n.update_state(frame)
        # n.remove_dead_nodes(dead_node_removed)

        # i = step in trace file = frame index... not really used for now
        i+=1
samples.to_csv('___.csv')


# # save to dataset to metric.__name__+".json"
# with open(metric.__name__+".json", 'w') as f:
#     json.dump(state, f)