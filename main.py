# create network
# load trace
# compute dijkstra+update network state for each packet
import csv
import json

from classes import Node, Link, Network

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
    return link._to.remaining_energy ** -1 # less energy => large cost

metric = metric_hop


#
# Create network/graph
#
for i in range(square_size):
    for j in range(square_size):
        print(i,j)
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

from utils import parse_trace_line

state = []
with open(trace_file) as f:
    i = 0
    for line in f:
        frame = parse_trace_line(line)
        # "transmit the frame"
        # - calculate shortest path
        _, path = n.shortest_path(source=n.get_node_by_id(SOURCE), destination=n.get_node_by_id(DESTINATION))
        # - save network state (topology, node state, link state, frame)
        for node in n.nodes:
            node.current_up=True if node.id in path else False
        n_state, l_state = n.get_state()
        # - update state of network (nodes in the path/outside the path, deplete energy according to state)
        # - - update link metric
        # - - update node energy (all in the path (times one for src/dst, only send OR recv), use UP current (times 2, recv and relay); rest, use DOWN/IDLE current)
        n.update_state(frame)
        
        
        state.append({
            'step':i,
            'frame':frame,
            'node_states': n_state,
            'link_state': l_state,
            'source_node_id': SOURCE,
            'source_node_id': DESTINATION,
            'path': path
        })
        # next
        i+=1


# save to dataset to metric.__name__+".json"
with open(metric.__name__+".json", 'w') as f:
    json.dump(state, f)

"""
To-do:
instead of saving entire dataset, save directly the samples/labels I want to try out!
"""