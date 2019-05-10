import pandas as pd

import networkx as nx
from networkx import shortest_path

from lib.functions.util import distance, any_packet_left_in_any_flow, generate_sample, neighborhood, flow_pair_generator
from lib.functions.aggregation import *
from lib.functions.sort import *
from lib.functions.metric import *
from lib.flow import TraceFlow, RandomFlow

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('num_flows', metavar='number_of_flows', type=int, nargs=1,
                    help='number of random fdisjoint flow pairs')
parser.add_argument('-o', '--output_file', dest='output_file', action='store', default='samples_test.csv',
                    help='output CSV filename')
parser.add_argument('-t', '--trace_file', dest='trace_file', action='store', default='mr_bean.dat',
                    help='input trace filename')
parser.add_argument('-r', '--random_trace', const=True, action='store_const', default=False,
                    help='input trace filename')
args = parser.parse_args()

NUMBER_OF_FLOWS = args.num_flows[0]
OUTPUT_CSV_NAME = args.output_file
TRACE_FILE = args.trace_file
RANDOM_TRACE = args.random_trace

SQUARE_SIZE=7
ENERGY_FRACTION_THRESHOLD = 0.02
DEAD_NODE_FLAG = False
METRIC_FUNCTION = metric_flow_counter

#
# Create graph
#
z=[]
for d_4 in range(510):
    z.append(4)
for d_3 in range(408):
    z.append(3)
for d_2 in range(82):
    z.append(2)

G = nx.random_degree_sequence_graph(z)
G.remove_edges_from(G.selfloop_edges())
while nx.is_connected(G) is False:
    G = nx.random_degree_sequence_graph(z)
    G.remove_edges_from(G.selfloop_edges())

G = G.to_directed()

for node in G.nodes:
    G.nodes[node]['id'] = node
    G.nodes[node]['position'] = (.0,.0,.0)
    G.nodes[node]['initial_charge'] = 150.
    G.nodes[node]['current_charge'] = 150.
    G.nodes[node]['energy_fraction'] = 1.
    G.nodes[node]['up'] = 1.7
    G.nodes[node]['down'] = .8
    G.nodes[node]['flow_counter'] = 0

for edge_data in G.edges.data():
    edge = edge_data[2]
    edge['from_node'] = edge_data[0]
    edge['to_node'] = edge_data[1]
    edge['error'] = 0.1
    edge['datarate'] = 1.0
    edge['distance'] = distance(G.nodes[edge_data[0]]['position'],
                                G.nodes[edge_data[1]]['position'])
    edge['metric'] = 1.0


#
# Create data flows
#
#
# Create data flows
#
src_dst_pairs = flow_pair_generator(G.nodes, NUMBER_OF_FLOWS)
data_flows = []
if RANDOM_TRACE:
    data_flows = [RandomFlow(pair[0], pair[1]) for pair in src_dst_pairs]
else:
    data_flows = [TraceFlow(pair[0], pair[1], TRACE_FILE) for pair in src_dst_pairs]
    
list_of_sources = [flow.from_node for flow in data_flows]


#
# Run simulation
#
samples = pd.DataFrame()
while any_packet_left_in_any_flow(data_flows):
    for flow in data_flows:
        if flow.has_packets_left is False:
            continue

        packet = flow.current_packet

        path = shortest_path(G, source=flow.from_node, target=flow.to_node, weight='metric')

        next_hop_index = 1
        for node_id in path[0:-1]:
            samples = samples.append(generate_sample(G, flow.current_packet, node_id, path[next_hop_index]), ignore_index=True)
            next_hop_index += 1
        
        # update state. reset current up state.
        next_hop_index = 1
        t = 0.0
        for node in path[0:-1]:
            from_node = path[next_hop_index-1]
            to_node = path[next_hop_index]
            next_hop_index += 1

            datarate = G.edges[from_node, to_node]['datarate']
            
            current = G.nodes[from_node]['up']
            initial_charge = G.nodes[from_node]['initial_charge']
            current_charge = G.nodes[from_node]['current_charge']

            packet_size = packet['size']
            t = (packet_size * 8) / (datarate * 1000000)  # seconds
            amount_to_decrease = (t * current)
            G.nodes[from_node]['current_charge'] = current_charge - amount_to_decrease
            G.nodes[from_node]['energy_fraction'] = G.nodes[from_node]['current_charge'] / G.nodes[from_node]['initial_charge']

        for node in path:
            if node in G:
                G.nodes[node]['flow_counter'] += 1

        for node in G.nodes:
            if node not in path:
                current = G.nodes[from_node]['down']
                initial_charge = G.nodes[node]['initial_charge']
                current_charge = G.nodes[node]['current_charge']

                amount_to_decrease = (t * current)
                G.nodes[node]['current_charge'] = current_charge - amount_to_decrease
                G.nodes[node]['energy_fraction'] = G.nodes[node]['current_charge'] / G.nodes[node]['initial_charge']

        for edge_data in G.edges.data():
            edge = edge_data[2]
            edge['metric'] = METRIC_FUNCTION(G, edge)
            edge['distance'] = distance(G.nodes[from_node]['position'], G.nodes[to_node]['position'])


    nodes_to_be_removed = []
    for node in G.nodes:
        if G.nodes[node]['energy_fraction'] <= ENERGY_FRACTION_THRESHOLD:
            nodes_to_be_removed.append(node)
            if node in list_of_sources:
                flow = next((x for x in data_flows if x.from_node == node), None)
                flow.kill_switch = True
    for node in nodes_to_be_removed:
        G.remove_node(node)

    for node in G.nodes:
        G.nodes[node]['flow_counter'] = 0

    # go to next packet
    for f in data_flows:
        f.next()


samples.to_csv(OUTPUT_CSV_NAME, index=False)
